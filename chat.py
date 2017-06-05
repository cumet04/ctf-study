import argparse
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, redirect, render_template

STATIC_PREFIX = 'ctf-study-xss'
API_PREFIX = 'ctf-study-xss/api/chat'
server = Flask(__name__, static_url_path='/%s' % STATIC_PREFIX)


def dbexec(query):
    # sqlite3のライブラリが、コネクション貼ったのと同一スレッドからでないと
    # 操作できない仕様になっているため、毎回コネクションを貼る
    with sqlite3.connect('./db/chat.db') as conn:
        cur = conn.cursor()
        cur.execute(query)
        return cur


@server.route('/%s/' % STATIC_PREFIX)
def static_redirect():
    return redirect('/%s/chat.html' % STATIC_PREFIX)


@server.route("/%s/chat.html" % STATIC_PREFIX)
def show_index():
    res = get_posts()
    if not isinstance(res, list):
        return res
    return render_template('chat.html', posts=res)


@server.route('/%s/posts' % API_PREFIX, methods=['GET'])
def api_list():
    res = get_posts()
    if not isinstance(res, list):
        return res
    return jsonify({'status': 'ok', 'posts': res})


def get_posts():
    cur = None
    try:
        cur = dbexec('SELECT id, name, timestamp, content from posts')
    except sqlite3.OperationalError as e:
        msg = '[ERROR] select failed: %s' % e
        print(msg)
        return jsonify({
            'status': 'error',
            'msg': msg
        }), 500

    posts = []
    for post_tup in cur.fetchall():
        posts.append({
            'id': post_tup[0],
            'name': post_tup[1],
            'timestamp': post_tup[2],
            'content': post_tup[3],
        })
    return posts


@server.route('/%s/posts' % API_PREFIX, methods=['POST'])
def api_post():
    data = request.json
    lack_param = []
    if 'name' not in data:
        lack_param.append('name')
    if 'content' not in data:
        lack_param.append('content')
    if lack_param:
        return jsonify({
            'status': 'error',
            'msg': "lack of parameter[s]: %s" % str(lack_param)
        }), 400

    timestr = (datetime.utcnow() + timedelta(hours=9)).strftime("%H:%M:%S")
    try:
        dbexec('''INSERT INTO posts (name, timestamp, content) VALUES (
            "%s", "%s", "%s")''' % (data['name'], timestr, data['content']))
    except sqlite3.OperationalError as e:
        msg = '[ERROR] insert value failed: %s' % e
        print(msg)
        return jsonify({
            'status': 'error',
            'msg': msg
        }), 500

    return api_list()


@server.route('/%s/delete' % API_PREFIX, methods=['GET'])
def api_delete():
    pid = request.args.get('id', default='', type=str)

    if pid == '':
        return jsonify({
            'status': 'error',
            'msg': "id is required"
        }), 400

    try:
        dbexec('DELETE FROM posts WHERE id = "%s"' % pid)
    except sqlite3.OperationalError as e:
        msg = '[ERROR] create table failed: %s' % e
        print(msg)
        return jsonify({
            'status': 'error',
            'msg': msg
        }), 500

    return jsonify({'status': 'ok'})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--host', type=str, default='127.0.0.1', help="serve host ip")
    parser.add_argument(
        '--port', type=int, default=50000, help="server's port")
    parser.add_argument(
        '--debug', action='store_true', help="run server with debug mode")
    parser.add_argument(
        '--initdb', action='store_true', help="force initialize db")
    params = parser.parse_args()

    if params.initdb:
        try:
            dbexec('''CREATE TABLE posts (
                id INTEGER NOT NULL PRIMARY KEY,
                name text NOT NULL,
                timestamp text NOT NULL,
                content text NOT NULL
                )''')
        except sqlite3.OperationalError as e:
            print('[ERROR] create table failed: %s' % e)
            return

    try:
        # CORS(server, resources={r"/*": {"origins": "*"}})
        server.run(host=params.host, port=params.port, debug=params.debug)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
