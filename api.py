from flask import Flask, jsonify, request
from OpenReview import func

app = Flask(__name__)
data = None  # 用于存储数据的变量

@app.route('/api/data', methods=['GET'])
def get_data():
    global data
    mode = int(request.args.get('mode', 1))  # 获取页码参数，默认为1

    if data is None:  # 如果数据还没有被爬取
        data = func(mode)

    return jsonify(data)  # 返回指定页的数据

if __name__ == '__main__':
    app.run(port=5000)