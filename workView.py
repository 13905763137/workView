from flask import Flask, render_template, request, g
from datetime import datetime
import os

import read_data
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib.image import imread

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def hello_world():
    if request.method == 'POST':
        zhiweis = request.form.get("zhiwei")
        zw = read_data.get_data(zhiweis)
        g.zw = zw
        return render_template("search.html")
    else:
        g.master = read_data.master
        g.doctor = read_data.doctor
        g.undergraduate = read_data.count_undergraduate
        g.others = read_data.others
        g.unlimited = read_data.unlimited
        g.college = read_data.college
        g.time = datetime.now()
        return render_template("education.html")


@app.route('/ciyun/', methods=["POST", "GET"])
def ciyun():
    if request.method == 'POST':
        zhiweis = request.form.get("zhiwei")
        zw = read_data.get_data(zhiweis)
        g.zw = zw
        return render_template("search.html")
    else:
        zw = read_data.get_cloud()
        data_dict = dict()
        for i in range(len(zw)):
            data_dict[zw[i][0]] = zw[i][1]
        show_sign(data_dict)
        return render_template("ciyun.html")


@app.route('/educate/', methods=["POST", "GET"])
def education():
    if request.method == 'POST':
        zhiweis = request.form.get("zhiwei")
        zw = read_data.get_data(zhiweis)
        g.zw = zw
        return render_template("search.html")
    else:
        g.master = read_data.master
        g.doctor = read_data.doctor
        g.undergraduate = read_data.count_undergraduate
        g.others = read_data.others
        g.unlimited = read_data.unlimited
        g.college = read_data.college
        g.time = datetime.now()
        return render_template("education.html")


@app.route('/salary/', methods=["POST", "GET"])
def salay():
    if request.method == 'POST':
        zhiweis = request.form.get("zhiwei")
        zw = read_data.get_data(zhiweis)
        g.zw = zw
        return render_template("search.html")
    else:
        data = read_data.get_salary()
        g.salay1 = data[0]
        g.salay2 = data[1]
        g.salay3 = data[2]
        g.salay4 = data[3]
        g.salay5 = data[4]
        return render_template("salay.html")


@app.route("/experience/", methods=["POST", "GET"])
def work_experience():
    if request.method == 'POST':
        zhiweis = request.form.get("zhiwei")
        zw = read_data.get_data(zhiweis)
        g.zw = zw
        return render_template("search.html")
    else:
        g.unrestricted = read_data.unrestricted
        g.one_year = read_data.one_year
        g.three_year = read_data.three_year
        g.five_year = read_data.five_year
        return render_template("experience.html")


@app.route("/areacity/", methods=["POST", "GET"])
def work_city():
    if request.method == 'POST':
        zhiweis = request.form.get("zhiwei")
        zw = read_data.get_data(zhiweis)
        g.zw = zw
        return render_template("search.html")
    else:
        city_data = read_data.get_areacity()
        city_data_list = []
        for i in range(len(city_data)):
            name = city_data[i][0]
            value = city_data[i][1]
            city_data_list.append((name, value))
        g.city_data_list = city_data_list
        return render_template("area_job.html")


def show_sign(content):
    # 设置词云属性
    BASE_DIR = os.path.dirname(__file__)
    color_mask = imread(os.path.join(BASE_DIR, 'bg.jpg'))
    wordcloud = WordCloud(font_path="simhei.ttf",  # 设置字体可以显示中文
                          # background_color="#fff",  # 背景颜色
                          max_words=1000,  # 词云显示的最大词数
                          mask=color_mask,  # 设置背景图片
                          max_font_size=100,  # 字体最大值
                          random_state=42,
                          width=1000, height=860, margin=2,
                          )

    wordcloud.generate_from_frequencies(content)
    # 从背景图片生成颜色值
    image_colors = ImageColorGenerator(color_mask)
    # 重新上色
    wordcloud.recolor(color_func=image_colors)
    # 保存图片
    wordcloud.to_file(os.path.join(BASE_DIR, 'static\cy.png'))


if __name__ == '__main__':
    app.run(debug=True)
