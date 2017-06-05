import argparse
from flask import Flask, request, redirect, render_template

URL_PREFIX = 'ctf-study-xss'
FILE_NAME = 'q0.html'
server = Flask(__name__, static_url_path='/%s' % URL_PREFIX)


@server.route('/%s/' % URL_PREFIX)
def static_redirect():
    return redirect('/%s/%s' % (URL_PREFIX, FILE_NAME))


@server.route('/%s/%s' % (URL_PREFIX, FILE_NAME), methods=['GET'])
def show():
    keyword = request.args.get('keyword', default='', type=str)
    return render_template(FILE_NAME, keyword=keyword)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', type=str, default='127.0.0.1', help="serve host ip")
    parser.add_argument(
        '--port', type=int, default=50000, help="server's port")
    parser.add_argument(
        '--debug', action='store_true', help="run server with debug mode")
    params = parser.parse_args()

    try:
        server.run(host=params.host, port=params.port, debug=params.debug)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
