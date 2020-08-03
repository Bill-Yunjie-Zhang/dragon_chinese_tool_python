import requests
import io
import unicodedata
from bs4 import BeautifulSoup
from bokeh.plotting import figure, output_file, show


def read_from_txt(file_name):
    text_file = open(file_name, "r", encoding="utf-8")
    lines = text_file.read().split('\n')
    text_file.close()
    return lines


def get_search_results_data(search):
    head = {"User-Agent": "Chrome/65.0.3325.181"}
    web_data = requests.get("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=" + search ,headers=head)

    unicodeData = web_data.text
    html = unicodedata.normalize('NFKD', unicodeData).encode('ascii', 'ignore')
    html_doc = html.decode("utf-8")

    soup = BeautifulSoup(html_doc, 'html.parser')
    mydivs = soup.findAll("span", {"class": "nums_text"})

    return mydivs[0].get_text()


def generate_search_results_list(list):
    search_results_list = []
    for shiju in list:
        search_results = int(get_search_results_data(shiju).replace(",", "")) / 10000
        search_results_list.append(search_results)
    return search_results_list


def main():
    name = input("输入文件名：")
    file_name = name + ".txt"
    sentences_list = read_from_txt(file_name)
    search_results_list = generate_search_results_list(sentences_list)

    output_file(name + '.html')

    p = figure(x_range=sentences_list, width_policy="max", height_policy="max")
    p.vbar(x=sentences_list, width=0.5, bottom=0, top=search_results_list, color="firebrick")

    p.title.text ='诗句搜索量'
    p.title.text_font_size = "20px"

    p.xaxis.axis_label = '诗句'
    p.yaxis.axis_label = '万次'

    show(p)

if __name__ == "__main__":
    main()