import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode, urlunparse, urlparse, parse_qsl

pd_dic = {"titles": [], "authors": [], "keywords": [], "pdfs": [], "abstract": []}
limit = 25
# 所有ICLR前%5的论文
url_0 = "https://api.openreview.net/notes?content.venue=ICLR+2023+notable+top+5%25&details=replyCount&offset=25&limit=25&invitation=ICLR.cc%2F2023%2FConference%2F-%2FBlind_Submission"
temp_resp_0 = requests.get(url_0)
count_0 = temp_resp_0.json()["count"]
# 所有ICLR前%25的论文
url_1 = "https://api.openreview.net/notes?content.venue=ICLR+2023+notable+top+25%25&details=replyCount&offset=0&limit=25&invitation=ICLR.cc%2F2023%2FConference%2F-%2FBlind_Submission"
temp_resp_1 = requests.get(url_1)
count_1 = temp_resp_1.json()["count"]
# 所有发表的论文
url_2 = "https://api.openreview.net/notes?content.venue=ICLR+2023+poster&details=replyCount&offset=0&limit=25&invitation=ICLR.cc%2F2023%2FConference%2F-%2FBlind_Submission"
temp_resp_2 = requests.get(url_2)
count_2 = temp_resp_2.json()["count"]
# 所有提交的论文
url_3 = "https://api.openreview.net/notes?content.venue=Submitted+to+ICLR+2023&details=replyCount&offset=0&limit=25&invitation=ICLR.cc%2F2023%2FConference%2F-%2FBlind_Submission"
temp_resp_3 = requests.get(url_3)
count_3 = temp_resp_3.json()["count"]
# desk-rejected-withdrawn-submissions
url_4 = "https://api.openreview.net/notes?details=replyCount%2Cinvitation%2Coriginal&offset=0&limit=25&invitation=ICLR.cc%2F2023%2FConference%2F-%2FWithdrawn_Submission"
temp_resp_4 = requests.get(url_4)
count_4 = temp_resp_4.json()["count"]


def get_one_page(_url, _dict):
    try:
        resp = requests.get(_url)
        resp.raise_for_status()  # 如果响应状态码不是200，就主动抛出异常
    except requests.RequestException as e:
        print(f"请求{_url}时发生错误：{e}")
        return

    notes = resp.json()["notes"]
    for note in notes:
        id = note["id"]
        content = note["content"]
        pdf = f"https://openreview.net/pdf?id={id}"
        _dict["titles"].append(content["title"])
        _dict["authors"].append(content["authors"])
        _dict["keywords"].append(content["keywords"])
        _dict["pdfs"].append(pdf)
        _dict["abstracts"].append(content["abstract"])
        print("ok")


def Thread_Method(__url, _count, _dict=pd_dic):
    with ThreadPoolExecutor(50) as t:
        for i in range(0, _count, limit):
            # 解析URL
            url_parts = list(urlparse(__url))
            # 解析查询参数
            query = dict(parse_qsl(url_parts[4]))
            # 更新offset参数
            query.update({"offset": str(i)})
            # 重新生成查询参数字符串
            url_parts[4] = urlencode(query)
            # 重新生成URL
            _url = urlunparse(url_parts)
            t.submit(get_one_page, _url, _dict)


def func(mode):
    dic = {"titles": [], "authors": [], "keywords": [], "pdfs": [], "abstracts": []}
    url = globals()["url_" + str(mode)]
    count = globals()["count_" + str(mode)]
    Thread_Method(url, count, dic)
    return dic


if __name__ == "__main__":
    pd_dic = func(4)
    db = pd.DataFrame(pd_dic)
    db.to_csv("desk-rejected-withdrawn-submissions.csv")
