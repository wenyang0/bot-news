# bot-news

该项目 主要用来实现 通过钉钉或者飞书机器人每天在群里 更新 新闻热搜，每日一言，当地天气和时间等情况


用法也非常简单，按照如下操作即可

第一步
```
下载本项目到本地
git clone https://github.com/wenyang0/bot-news.git

```

第二步
```
修改 飞书 或者 钉钉脚本中的机器人的webhook地址

钉钉：
# 配置钉钉机器人 Webhook URL
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_ACCESS_TOKEN"

飞书：
# 配置飞书机器人 Webhook URL
webhook_url = "YOUR_WEBHOOK_URL"


```
第三步
```
执行python脚本
钉钉群：
python3  dingding-news.py

飞书群：
python3  feishu-news.py
```

第四步
去钉钉或者飞书群里查看效果

钉钉：
![钉钉群图片](./dingding.png)


飞书：
![飞书群图片](./feishu.png)
