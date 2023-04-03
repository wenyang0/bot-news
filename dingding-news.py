import json
import requests
from datetime import datetime

# 配置钉钉机器人 Webhook URL
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN"

# 获取新闻消息列表
url = "https://api.1314.cool/getbaiduhot/"
response = requests.get(url).json()
news_list = response["data"]

# 创建新闻字典并写入到 JSON 文件中
news_items = []
for news in news_list:
    if "word" not in news or "url" not in news:
        continue
    item = {"title": news['word'], "messageURL": news['url']}
    news_items.append(item)
with open("news.json", "w") as f:
    json.dump({"data": news_items}, f, ensure_ascii=False)

print("新闻数据已写入到 news.json 文件中。")

# 获取当前日期和时间
now = datetime.now()

# 使用第三方API获取当天天气情况
url = "http://wttr.in/nanning?format=%C+%t"
response = requests.get(url).text
weather_info = response.strip().split(' ')
temperature = weather_info[-1]
weather = weather_info[0]

# 使用金山词霸API获取每日一句（注：需要联网）
url = "http://open.iciba.com/dsapi/"
response = requests.get(url).json()
daily_sentence = response["note"]
encouraging_words = ""  # 鼓励自己的话

# 读取 JSON 文件
with open("news.json", "r") as f:
    news_data = json.load(f)

# 获取新闻消息列表
news_list = news_data["data"]

# 初始化一个空列表来存储所有新闻消息的字典
news_items = []

# 遍历新闻消息列表，创建新闻字典并添加到列表中
count = 0
for news in news_list:
    if count == 10:
        break
    item = {
        "title": news["title"],
        "actionURL": news["messageURL"]
    }
    news_items.append(item)
    count += 1

# 拼接钉钉卡片消息内容
message = {
    "msgtype": "actionCard",
    "actionCard": {
        "title": f"今日热搜排行版及天气情况 {now.month}月{now.day}日",
        "text": f"""今天是 {now.month}月{now.day}日，南宁市的天气是 {temperature}℃，{weather}。

每日一句：{daily_sentence}

<font color=#E47B3F size=3>注意：</font> 新闻来自百度热搜榜前十，内容仅供参考。""",
        "btnOrientation": "1",
        "btns": []
    }
}

# 添加每个新闻消息到消息内容中
for news in news_items:
    item = {
        "title": news["title"],
        "actionURL": news["actionURL"]
    }
    message["actionCard"]["btns"].append(item)

# 发送钉钉卡片消息
headers = {'Content-Type': 'application/json; charset=utf-8'}
response = requests.post(webhook_url, headers=headers, data=json.dumps(message))

# 检查响应状态码
if response.status_code != 200:
    print("发送钉钉卡片消息失败：", response.text)
else:
    print("发送钉钉卡片消息成功！")
