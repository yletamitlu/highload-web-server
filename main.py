from utils import parser, consts
from server import server


if __name__ == '__main__':
    parser.config_to_map(consts.CONFIG_PATH)
    server = server.Server()
    server.init_connect()
    server.prefork()
