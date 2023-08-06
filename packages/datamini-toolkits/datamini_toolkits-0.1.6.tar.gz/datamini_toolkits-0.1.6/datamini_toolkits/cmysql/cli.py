import argparse
from .agent import ChatMySQLCLI
from .logs import log


def get_args():
    parser = argparse.ArgumentParser(description='Chat MySQL CLI', add_help=False)


    # 添加参数选项
    parser.add_argument('database', nargs='?', help='Name of the database')


    parser.add_argument('-h', '--host', dest='host', metavar='host', help='Connect to host.')
    parser.add_argument('-u', '--user', dest='user', metavar='user', help='User for login')
    parser.add_argument('-p', '--password', dest='password', nargs='?', const='name',
                        help='Password to use when connecting to server. If password is not given, it\'s asked from the tty.')
    parser.add_argument('-P', '--port', dest='port', type=int, default=3306,
                        help='Port number to use for connection, default (3306).')
    parser.add_argument('--help', action='help',
                        help='Show this help message and exit.')  # 添加自定义的帮助选项

    # 解析命令行参数
    args = parser.parse_args()
    return args


def get_db_uri_from_args(args):
    db_host = args.host or "127.0.0.1"
    db_port = int(args.port) or 3306
    db_user = args.user or "root"
    db_password = args.password or ""
    db_name = args.database or "test"

    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return db_uri



def main():
    args = get_args()
    db_uri = get_db_uri_from_args(args)

    cmysql = ChatMySQLCLI(db_uri)

    while True:
        request = input("""
cmysql> """)

        with cmysql.get_llm_callback() as cb:
            cmysql.agent.run(request)
            log.llm_billing(request, cb)


if __name__ == "__main__":
    main()
