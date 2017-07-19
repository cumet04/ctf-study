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
    res1 = resp(keyword)
    res = make_response(resp(keyword, str(res1)))
    res.set_cookie('flag', value="cookies are here !",
                   secure=None, httponly=False)
    return res


def resp_0(keyword, source=""):
    return render_template('search.html', keyword=keyword, source=source)


def resp_1(keyword, source=""):
    if keyword.startswith('<script>') and keyword.endswith('</script>'):
        keyword = keyword[8:-9]
    return render_template('search.html', keyword=keyword, source=source)


def resp_2(keyword, source=""):
    keyword = keyword.replace('<', '&lt;')
    keyword = keyword.replace('>', '&gt;')
    return render_template('search.html', keyword=keyword, source=source)


def resp_3(keyword, source=""):
    keyword = keyword.replace('<', '&lt;')
    keyword = keyword.replace('>', '&gt;')
    return render_template('search2.html', keyword=keyword, source=source)


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
                   debug=params.debug, threaded=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
