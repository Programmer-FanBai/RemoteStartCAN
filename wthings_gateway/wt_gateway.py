# #!/opt/python3/bin/python3
# # -*- coding: UTF-8 -*-

from os import path, listdir, mkdir, curdir
import sys
sys.path.append("/tmp/pycharm_project_382")
from wthings_gateway.gateway.wt_gateway_service import WTGatewayService


def main():
    if "logs" not in listdir(curdir):
        mkdir("logs")
    WTGatewayService(path.dirname(path.abspath(__file__)) + '/config/wt_gateway.yaml'.replace('/', path.sep))


def daemon():
    WTGatewayService("/etc/wthings-gateway/config/wt_gateway.yaml".replace('/', path.sep))


if __name__ == '__main__':
    main()
