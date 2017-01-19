/**
 * Copyright © ${project.inceptionYear}-2017 The Thingsboard Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.thingsboard.gateway.service;

import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import lombok.extern.slf4j.Slf4j;
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.internal.security.SSLSocketFactoryFactory;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.thingsboard.server.common.data.kv.KvEntry;
import org.thingsboard.server.common.data.kv.TsKvEntry;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.UUID;
import java.util.function.Consumer;
import java.util.stream.Collectors;

import static org.thingsboard.gateway.util.JsonTools.*;

/**
 * Created by ashvayka on 16.01.17.
 */
@Service
@Slf4j
public class MqttGatewayService implements GatewayService {

    private final UUID clientId = UUID.randomUUID();

    @Autowired
    private MqttGatewayConfiguration configuration;

    private MqttAsyncClient tbClient;
    private MqttConnectOptions tbClientOptions;

    @PostConstruct
    public void init() throws Exception {
        tbClientOptions = new MqttConnectOptions();
        tbClientOptions.setCleanSession(true);

        MqttGatewaySecurityConfiguration security = setupSecurityOptions(tbClientOptions);

        tbClient = new MqttAsyncClient((security.isSsl() ? "ssl" : "tcp") + "://" + configuration.getHost() + ":" + configuration.getPort(),
                clientId.toString(), new MemoryPersistence());
        connect();
    }

    @PreDestroy
    public void preDestroy() throws Exception {
        tbClient.disconnect();
    }

    @Override
    public void connect(final String deviceName) {
        byte[] msgData = toBytes(newNode().put("name", deviceName));
        MqttMessage msg = new MqttMessage(msgData);
        publishSync("v1/gateway/connect", msg,
                token -> log.info("[{}] Device Connected!", deviceName),
                error -> log.warn("[{}] Failed to report device connection!", deviceName, error));
    }

    @Override
    public void disconnect(String deviceName) {
        byte[] msgData = toBytes(newNode().put("name", deviceName));
        MqttMessage msg = new MqttMessage(msgData);
        publishSync("v1/gateway/disconnect", msg,
                token -> log.info("[{}] Device Disconnected!", deviceName),
                error -> log.warn("[{}] Failed to report device disconnect!", deviceName, error));
    }

    @Override
    public void onDeviceAttributesUpdate(String deviceName, List<KvEntry> attributes) {
        log.info("[{}] Updating device attributes: {}", deviceName, attributes);
        ObjectNode node = newNode();
        ObjectNode deviceNode = node.putObject(deviceName);
        attributes.forEach(kv -> putToNode(deviceNode, kv));
        byte[] msgData = toBytes(node);
        MqttMessage msg = new MqttMessage(msgData);
        publishAsync("v1/gateway/attributes", msg,
                token -> log.debug("[{}] Device attributes published!", deviceName),
                error -> log.warn("[{}] Failed to report device attributes!", deviceName, error));
    }

    @Override
    public void onDeviceTimeseriesUpdate(String deviceName, List<TsKvEntry> telemetry) {
        log.info("[{}] Updating device telemetry: {}", deviceName, telemetry);
        ObjectNode node = newNode();
        Map<Long, List<TsKvEntry>> tsMap = telemetry.stream().collect(Collectors.groupingBy(v -> v.getTs()));
        ArrayNode deviceNode = node.putArray(deviceName);
        tsMap.entrySet().forEach(kv -> {
            Long ts = kv.getKey();
            ObjectNode tsNode = deviceNode.addObject();
            tsNode.put("ts", ts);
            ObjectNode valuesNode = tsNode.putObject("values");
            kv.getValue().forEach(v -> putToNode(valuesNode, v));
        });
        byte[] msgData = toBytes(node);
        MqttMessage msg = new MqttMessage(msgData);
        publishAsync("v1/gateway/telemetry", msg,
                token -> log.debug("[{}] Device telemetry published!", deviceName),
                error -> log.warn("[{}] Failed to publish device telemetry!", deviceName, error));

    }

    private void connect() throws MqttException, InterruptedException {
        while (!tbClient.isConnected()) {
            log.info("Attempt to connect to Thingsboard!");
            tbClient.connect(tbClientOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken iMqttToken) {
                    log.info("Connected to Thingsboard!");
                }

                @Override
                public void onFailure(IMqttToken iMqttToken, Throwable e) {
                    log.info("Failed to connect to Thingsboard!", e);
                }
            }).waitForCompletion();
            if (!tbClient.isConnected()) {
                Thread.sleep(configuration.getRetryInterval());
            }
        }
    }

    private void publishAsync(final String topic, MqttMessage msg, Consumer<IMqttToken> onSuccess, Consumer<Throwable> onFailure) {
        publish(topic, msg, false, onSuccess, onFailure);
    }

    private void publishSync(final String topic, MqttMessage msg, Consumer<IMqttToken> onSuccess, Consumer<Throwable> onFailure) {
        publish(topic, msg, true, onSuccess, onFailure);
    }

    private void publish(final String topic, MqttMessage msg, boolean sync, Consumer<IMqttToken> onSuccess, Consumer<Throwable> onFailure) {
        try {
            IMqttDeliveryToken token = tbClient.publish(topic, msg, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    onSuccess.accept(asyncActionToken);
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable e) {
                    onFailure.accept(e);
                }
            });
            if (sync) {
                token.waitForCompletion();
            }
        } catch (MqttException e) {
            onFailure.accept(e);
        }
    }


    private MqttGatewaySecurityConfiguration setupSecurityOptions(MqttConnectOptions options) {
        MqttGatewaySecurityConfiguration security = configuration.getSecurity();
        if (security.isTokenBased()) {
            options.setUserName(security.getAccessToken());
            if (!StringUtils.isEmpty(security.getTruststore())) {
                Properties sslProperties = new Properties();
                sslProperties.put(SSLSocketFactoryFactory.TRUSTSTORE, security.getTruststore());
                sslProperties.put(SSLSocketFactoryFactory.TRUSTSTOREPWD, security.getTruststorePassword());
                sslProperties.put(SSLSocketFactoryFactory.TRUSTSTORETYPE, "JKS");
                sslProperties.put(SSLSocketFactoryFactory.CLIENTAUTH, false);
                options.setSSLProperties(sslProperties);
            }
        } else {
            Properties sslProperties = new Properties();
            sslProperties.put(SSLSocketFactoryFactory.KEYSTORE, security.getKeystore());
            sslProperties.put(SSLSocketFactoryFactory.KEYSTOREPWD, security.getKeystorePassword());
            sslProperties.put(SSLSocketFactoryFactory.KEYSTORETYPE, "JKS");
            sslProperties.put(SSLSocketFactoryFactory.TRUSTSTORE, security.getTruststore());
            sslProperties.put(SSLSocketFactoryFactory.TRUSTSTOREPWD, security.getTruststorePassword());
            sslProperties.put(SSLSocketFactoryFactory.TRUSTSTORETYPE, "JKS");
            sslProperties.put(SSLSocketFactoryFactory.CLIENTAUTH, true);
            options.setSSLProperties(sslProperties);
        }
        return security;
    }
}