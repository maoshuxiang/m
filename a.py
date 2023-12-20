import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from pyecharts.charts import Bar, Pie, Line, Radar
from pyecharts import options as opts
from pyecharts.charts import WordCloud


def main():
    # 设置 Streamlit 应用的标题
    st.title('Python 爬虫可视化')

    # 创建一个文本输入框，用于接收用户输入的要爬取的网站地址
    url = st.text_input('请输入要爬取的网站地址：')

    # 如果用户已经输入了网址
    if url:
        # 发送 GET 请求获取指定网站的内容
        res = requests.get(url)
        encoding = res.encoding if 'charset' in res.headers.get('content-type', '').lower() else None

        # 使用 BeautifulSoup 将网站内容解析为 BeautifulSoup 对象
        soup = BeautifulSoup(res.content, 'html.parser', from_encoding=encoding)

        # 获取网站文本内容
        text = soup.get_text()

        # 使用 jieba 库进行中文分词处理
        words = [word for word in jieba.cut(text) if len(word) >= 2 and '\u4e00' <= word <= '\u9fff']

        # 使用 Counter 类统计词语出现的次数
        word_counts = Counter(words)

        # 创建一个下拉框，用于选择要呈现的图表类型
        chart_type = st.selectbox('请选择要呈现的图表类型：', ['饼状图', '条形图', '折线图', '词云图', '雷达图'])

        # 生成饼状图
        if chart_type == '饼状图':
            c = (
                Pie()
                .add("", word_counts.most_common(10))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                .render("pie_chart.html")
            )
            st.components.v1.html(open('pie_chart.html', 'r', encoding='utf-8').read(), height=600)

        # 生成条形图
        elif chart_type == '条形图':
            x_axis = [x[0] for x in word_counts.most_common(10)]
            y_axis = [x[1] for x in word_counts.most_common(10)]
            c = (
                Bar()
                .add_xaxis(x_axis)
                .add_yaxis("", y_axis)
                .set_global_opts(title_opts=opts.TitleOpts(title="条形图"))
                .render("bar_chart.html")
            )
            st.components.v1.html(open('bar_chart.html', 'r', encoding='utf-8').read(), height=600)

        # 生成折线图
        elif chart_type == '折线图':
            x_axis = [x[0] for x in word_counts.most_common(10)]
            y_axis = [x[1] for x in word_counts.most_common(10)]
            c = (
                Line()
                .add_xaxis(x_axis)
                .add_yaxis("", y_axis, is_smooth=True)
                .set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
                .render("line_chart.html")
            )
            st.components.v1.html(open('line_chart.html', 'r', encoding='utf-8').read(), height=600)

        # 生成词云图
        elif chart_type == '词云图':
            words_dict = {w[0]: w[1] for w in word_counts.most_common(20)}
            c = (
                WordCloud()
                .add("", [list(w) for w in words_dict.items()])
                .set_global_opts(title_opts=opts.TitleOpts(title="词云图"))
                .render("wordcloud_chart.html")
            )
            st.components.v1.html(open('wordcloud_chart.html', 'r', encoding='utf-8').read(), height=600)

        # 生成雷达图
        elif chart_type == '雷达图':
            data_pair = word_counts.most_common(10)
            c = (
                Radar()
                .add_schema(
                    schema=[
                        opts.RadarIndicatorItem(name=d[0], max_=d[1]) for d in data_pair
                    ]
                )
                .add("词频统计", [data_pair], color="#ff6666")
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="雷达图"))
                .render("radar_chart.html")
            )
            st.components.v1.html(open('radar_chart.html', 'r', encoding='utf-8').read(), height=600)


if __name__ == '__main__':
    main()