import argparse
from flask import Flask, request, redirect, render_template, make_response

URL_PREFIX = 'ctf-study-xss'
FILE_NAME = 'q.html'
server = Flask(__name__, static_url_path='/%s' % URL_PREFIX)


@server.route('/%s/' % URL_PREFIX)
def static_redirect():
    return redirect('/%s/%s' % (URL_PREFIX, FILE_NAME))


@server.route('/%s/%s' % (URL_PREFIX, FILE_NAME), methods=['GET'])
def show():
    keyword = request.args.get('keyword', default='', type=str)
    res = make_response(render_template(
        'search.html', keyword=sanitize(keyword)))
    res.set_cookie('flag', value="cookies are here !",
                   secure=None, httponly=False)
    return res


def sanitize_0(keyword):
    return keyword


def sanitize_1(keyword):
    if keyword.startswith('<script>') and keyword.endswith('</script>'):
        keyword = keyword[8:-9]
    return keyword


def sanitize_2(keyword):
    keyword = keyword.replace('<', '&lt;')
    keyword = keyword.replace('>', '&gt;')
    return keyword


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', type=str, default='127.0.0.1', help="serve host ip")
    parser.add_argument(
        '--port', type=int, default=50000, help="server's port")
    parser.add_argument(
        '--debug', action='store_true', help="run server with debug mode")
    parser.add_argument(
        '--sanitize', type=int, default=0, help="sanitize level")
    params = parser.parse_args()

    funcs = [sanitize_0, sanitize_1, sanitize_2]
    global sanitize
    sanitize = funcs[params.sanitize]

    try:
        server.run(host=params.host, port=params.port, debug=params.debug)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
