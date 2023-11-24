from flask import Flask, jsonify, request, send_file
from flask_cors import cross_origin
from OpenReview import func
from wordcloud import WordCloud
from io import BytesIO

app = Flask(__name__)
data = None

@app.route('/api/data', methods=['GET'])
@cross_origin()
def get_data():
    mode = int(request.args.get('mode'))

    global data
    data = func(mode)

    return jsonify(data)  # 返回指定页的数据

@app.route('/api/keywords-wordcloud', methods=['GET'])
@cross_origin()
def generate_keywords_wordcloud():
    global data
    flat_list = []
    for item in data['keywords']:
        for words in item:
            flat_list.append(words)
    keywords_text = ",".join(flat_list)

    # 生成词云
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords_text)

    # 保存词云为图片
    img_buffer = BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)

    return send_file(img_buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(port=5000)