# -*- coding: utf-8 -*-


import argparse

from venus912_dashboard import _version

from .template_handler import template_handler
from .server_handler import server_handler
from .db_handler import db_handler


def create_parser():
    parser = argparse.ArgumentParser(description='venus912_dashboard command')
    parser.add_argument(
        '--version', '-v', action='version', version=_version.__version__)
    subparsers = parser.add_subparsers()

    # template
    parser_template = subparsers.add_parser(
        'template', help='see `venus912_dashboard template -h`')
    parser_template.add_argument(
        '--dir', required=False, help='Optional destination directory', default='./')
    parser_template.set_defaults(handler=template_handler)

    # server
    parser_server = subparsers.add_parser(
        'server', help='see `venus912_dashboard server -h`')
    parser_server.add_argument(
        '-H', '--host', required=False, help='host', default='0.0.0.0')
    parser_server.add_argument(
        '-p', '--port', required=False, type=int, help='port')
    parser_server.add_argument(
        '--settings', required=False, help='settings YAML. See https://github.com/venus912/dashboard/blob/master/venus912_dashboard/template/settings.yml-tpl')
    parser_server.add_argument(
        '--logger', required=False, help='Python file of your custom logger. Need to inherit "logger_interface.py". See https://github.com/venus912/dashboard/blob/master/venus912_dashboard/logger/logger_interface.py')
    parser_server.add_argument(
        '--debug', required=False, type=bool, help='Debug mode.')
    parser_server.add_argument(
        '--kube_config_dir', required=False, help='Directory of kube_config files.')
    parser_server.add_argument(
        '--db_mode', required=False, help='Dashboard DB mode. One of [sqlite/mysql]. Default "sqlite".')
    parser_server.add_argument(
        '--db_host', required=False, help='Dashboard MySQL host. Necessary if "--db_mode mysql".')
    parser_server.add_argument(
        '--db_port', required=False, type=int, help='Dashboard MySQL port. Necessary if "--db_mode mysql".')
    parser_server.add_argument(
        '--db_name', required=False, help='Dashboard MySQL DB name. Necessary if "--db_mode mysql".')
    parser_server.add_argument(
        '--db_username', required=False, help='Dashboard MySQL username. Necessary if "--db_mode mysql".')
    parser_server.add_argument(
        '--db_password', required=False, help='Dashboard MySQL password. Necessary if "--db_mode mysql".')
    parser_server.set_defaults(handler=server_handler)

    # db
    parser_db = subparsers.add_parser(
        'db', help='see `venus912_dashboard db -h`')
    parser_db.add_argument(
        'type', choices=['init', 'revision', 'migrate', 'edit', 'merge',
                         'upgrade', 'downgrade', 'show', 'history', 'heads',
                         'branches', 'current', 'stamp'])
    parser_db.add_argument(
        '--settings', required=False, help='settings YAML. See https://github.com/venus912/dashboard/blob/master/venus912_dashboard/template/settings.yml-tpl')
    parser_db.add_argument(
        '--logger', required=False, help='Python file of your custom logger. Need to inherit "logger_interface.py". See https://github.com/venus912/dashboard/blob/master/venus912_dashboard/logger/logger_interface.py')
    parser_db.add_argument(
        '--db_mode', required=False, help='Dashboard DB mode. One of [sqlite/mysql]. Default "sqlite".')
    parser_db.add_argument(
        '--db_host', required=False, help='Dashboard MySQL host. Necessary if "--db_mode mysql".')
    parser_db.add_argument(
        '--db_port', required=False, type=int, help='Dashboard MySQL port. Necessary if "--db_mode mysql".')
    parser_db.add_argument(
        '--db_name', required=False, help='Dashboard MySQL DB name. Necessary if "--db_mode mysql".')
    parser_db.add_argument(
        '--db_username', required=False, help='Dashboard MySQL username. Necessary if "--db_mode mysql".')
    parser_db.add_argument(
        '--db_password', required=False, help='Dashboard MySQL password. Necessary if "--db_mode mysql".')
    parser_db.set_defaults(handler=db_handler)

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    if hasattr(args, 'handler'):
        args.handler(vars(args))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
