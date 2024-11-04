import time

from functools import wraps
from flask import Flask, request, jsonify
import jwt
from jwt import ExpiredSignatureError

app = Flask(__name__)

max_time = 60
refresh_max_time = 120
token_secret = "This is a secret"


def verify_token(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            token = request.headers["token"]
            print(token)
            data = jwt.decode(token, token_secret, algorithms=['HS256'])
            print(f"=====data=========={data}")
            now = int(time.time())
            time_interval = now - data['time']

            if time_interval >= max_time:
                # create new token
                token, refresh_token = creat_token()
                return jsonify({"token": token, "refresh_token": refresh_token})
        except ExpiredSignatureError:
            return "Token expired"
        except Exception as ex:
            print(ex)
            return "Login again"

        return func(*args, **kwargs)

    return decorator


def creat_token(uid):
    now = int(time.time())
    payload = {'uid': uid, 'time': now, 'exp': now + max_time}
    refresh_payload = {'uid': uid, 'time': now, 'exp': now + refresh_max_time}
    token = jwt.encode(payload, token_secret, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, token_secret, algorithm='HS256')
    return token, refresh_token


@app.route('/login', methods=["POST"])
def login():
    user_name = request.values.get('user_name')
    password = request.values.get('password')
    # @TODO 根据user_name和password 获取唯一的uid
    uid = 10
    token, refresh_token = creat_token(uid=uid)
    return jsonify({"token": token, "refresh_token": refresh_token})


# 在header中设置token请求
@app.route('/test', methods=['GET'])
@verify_token
def test():
    return 'hello world'


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5000)
    app.run(port=5000)
