import json
import requests
from datetime import datetime


# 获取新闻消息列表
url = "https://api.1314.cool/getbaiduhot/"
response = requests.get(url).json()
news_list = response["data"]

# 创建新闻字典并写入到 JSON 文件中
news_items = [{"word": news['word'], "url": news['url']} for news in news_list]
with open("news.json", "w") as f:
    json.dump({"data": news_items}, f, ensure_ascii=False)

print("新闻数据已写入到 news.json 文件中。")


# 配置飞书机器人 Webhook URL
webhook_url = "YOUR_WEBHOOK_URL"

# 获取当前日期和时间
now = datetime.now()

# 使用第三方API获取当天天气情况
url = "http://wttr.in/%E5%8C%97%E4%BA%AC?format=%C+%t"
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
        "title": news["word"],
        "content": news["url"]
    }
    news_items.append(item)
    count += 1

# 拼接飞书消息内容
message = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True,
            "enable_forward": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "今日热搜排行版及天气情况",
                "color": "#007FFF",
                "size": "lg",
                "bold": True
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"今天是 **{now.month}月{now.day}日**，天气 {temperature}℃，{weather}。"
                }
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"每日一句：{daily_sentence}\n\n{encouraging_words}"
                }
            },
            {
                "tag": "hr"
            }
        ]
    }
}

# 添加每个新闻消息到消息内容中
for news in news_items:
    item = {
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"**[{news['title']}]({news['content']})**"
        }
    }
    message["card"]["elements"].append(item)

# 发送飞书消息
response = requests.post(webhook_url, json=message)

# 检查响应状态码
if response.status_code != 200:
    print("发送飞书消息失败：", response.text)
else:
    print("发送飞书消息成功！")
