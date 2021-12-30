# 超星自動每日健康

### 簡介

自動填寫天津科技大學每日超星每日健康，可以使用GitHub Action自動打卡

### 配置

#### 第一步

打開 `send.py` 找到

```
def __init__(self, rece=None, title=None, uid=None, mail_host="發信站地址", mail_user="發信郵箱地址例如123@gmail.com", mail_pass="發送密碼", sender="跟mail_user寫一樣就好"):
```

按照提示寫好email發信地址

#### 第二步

打開 `main.py` 找到

```
sender = Send(rece="12345678@qq.com")
```

後面 `rece` 參數改成你的郵箱地址

#### 第三步

打開 `account.json` 配置超星用戶信息

```
[
  {
    "username": "用戶名(手機號)",
    "password": "密碼",
    "information": {
      "name": "你的名字",
      "number": "這裏寫8位學號",
      "college": "這裏寫學院，例如：人工智能学院",
      "education": "這裏改成學位，例如：本科",
      "grade": "這裏改成年級，例如：本一"
    }
  },
  {
    "username": "13000000000",
    "password": "a123456A",
    "information": {
      "name": "我是範例",
      "number": 21104101,
      "college": "人工智能学院",
      "education": "本科",
      "grade": "本一"
    }
  }
]
```

按照提示配置你的信息，如果只是一個人使用的話，請刪掉第二組信息，亦可以添加別人的信息一并進行打卡，注意編輯完成后花括弧后不要留有多餘的 `,` 

### 配置GitHub自動提交

首先在Action裏面創建新的 `workflow` 

然後在配置文件中進行配置

這裏給出我的配置文件以供參考

```
on:
  push:
  schedule:
  # 設定定時執行的時間
  # 格式為:分鐘 小時 天 月 周
  # LinuxCron的時間表達式(*代表每)，以下表達式代表：每月每周每天 0:25運行
  # 注意:GitHub伺服器為UTC時間，即中國大陸時間向前推算8小時
    - cron: '25 16 * * *'
    - cron: '25 4 * * *'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.10
      uses: actions/setup-python@v2
      with:
        python-version: "3.10"
    - name: Install dependencies
      run: |
        python3 -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi
    - name: Run The Script
      run: |
        sudo timedatectl set-timezone Asia/Taipei
        python3 main.py
```

`sudo timedatectl set-timezone Asia/Taipei` 的意義為設定虛擬編譯運行環境的時區，防止提交的時間發生時區錯誤。
！！！！注意：一定要將項目設定為Private，否則別人能看到你的超星學習通賬號及密碼！！！！

### 二次開發

本程式亦可作爲模組導入其他Python脚本，你可以調用main.py中的req類完成你自己的實現
