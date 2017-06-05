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
    res = make_response(resp(keyword))
    res.set_cookie('flag', value="cookies are here !",
                   secure=None, httponly=False)
    return res


def resp_0(keyword):
    return render_template('search.html', keyword=keyword)


def resp_1(keyword):
    if keyword.startswith('<script>') and keyword.endswith('</script>'):
        keyword = keyword[8:-9]
    return render_template('search.html', keyword=keyword)


def resp_2(keyword):
    keyword = keyword.replace('<', '&lt;')
    keyword = keyword.replace('>', '&gt;')
    return render_template('search.html', keyword=keyword)


def resp_3(keyword):
    keyword = keyword.replace('<', '&lt;')
    keyword = keyword.replace('>', '&gt;')
    return render_template('search2.html', keyword=keyword)


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

    funcs = [resp_0, resp_1, resp_2, resp_3]
    global resp
    resp = funcs[params.sanitize]

    try:
        server.run(host=params.host, port=params.port,
                   debug=params.debug)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
