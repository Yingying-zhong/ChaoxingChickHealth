import base64
import json
import os
import re
import sys
import time
from urllib import parse
from send import Send
import requests

from spawn_fake_image import spawn_fake_image


class req(object):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://passport2.chaoxing.com/login?fid=1856',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    cookie = dict()

    # tmp_path = os.path.dirname(os.path.realpath(sys.argv[0])) + "/tmp/"
    # 這裏是默認信息，不改無所謂
    def __init__(self, uname, pwd, name="姓名", num=21100000, college="人工智能学院", education="本科", grade="本一"):
        # self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.form_data = None
        self.name = name
        self.num = num
        self.uname = uname
        self.college = college
        self.education = education
        self.grade = grade
        self.data_code = None
        self.health_code = None
        self.session = requests.session()
        self.login_f = {
            'fid': -1,
            'uname': str(uname),
            'password': self.encrypt(str(pwd)),
            'refer': "http://i.chaoxing.com",
            't': 'true'
        }

    def encrypt(self, o_input):
        return base64.b64encode(o_input.encode()).decode()

    def login(self):
        url = "http://passport2.chaoxing.com/fanyalogin"
        r = self.session.post(url, data=self.login_f, headers=self.headers, )
        self.cookie.update(requests.utils.dict_from_cookiejar(r.cookies))
        res = json.loads(r.text)
        if res['status']:
            return 0
        else:
            return res

    def make_form(self):
        with open('resource/template.json', encoding='utf-8') as f:
            data = json.load(f)
        for i in range(len(data)):
            try:
                lable = data[i]['fields'][0]['label']
                # print(lable)
                # print(str(self.num)[0:6])
                if lable == "填写日期":
                    t = time.strftime("%Y-%m-%d", time.localtime())
                    data[i]['fields'][0]['values'][0]['val'] = t
                elif lable == "学号":
                    data[i]['fields'][0]['values'][0]['val'] = str(self.num)
                elif lable == "姓名":
                    data[i]['fields'][0]['values'][0]['val'] = self.name
                elif lable == "所属学院":
                    data[i]['fields'][0]['values'][0]['val'] = self.college
                elif lable == "学历层次":
                    data[i]['fields'][0]['values'][0]['val'] = self.education
                elif lable == "所属年级":
                    data[i]['fields'][0]['values'][0]['val'] = self.grade
                elif lable == "所属班级":
                    data[i]['fields'][0]['values'][0]['val'] = str(self.num)[0:6]
                elif lable == "联系方式":
                    data[i]['fields'][0]['values'][0]['val'] = str(self.uname)
                elif lable == "今日健康码截图":
                    self.health_code['data']['size'] = str(round(request1.health_code['data']['size'] / 1000, 2)) + "KB"
                    data[i]['fields'][0]['values'][0] = self.health_code['data']
                elif lable == "今日行程码截图":
                    self.data_code['data']['size'] = str(round(request1.data_code['data']['size'] / 1000, 2)) + "KB"
                    data[i]['fields'][0]['values'][0] = self.data_code['data']
            except Exception as e:
                lable = data[i]['label']
        self.form_data = data
        return data

    def sand(self):
        self.session = requests.session()
        url = "https://uc.chaoxing.com/mobileSet/homePage?fid=121890"
        r = self.session.get(url, headers=self.headers, cookies=self.cookie)
        self.cookie.update(requests.utils.dict_from_cookiejar(r.cookies))
        data = {'mAppId': 5298819}
        url = "https://uc.chaoxing.com/mobile/addAppVisit"
        self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
        data = {'id': 85387, 'mAppId': 5298819}
        url = "https://uc.chaoxing.com/mobile/getTallyInfo?id=85387&mAppId=5298819"
        r = self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
        infodata = json.loads(r.text)
        # print(infodata)
        # print(self.cookie)
        if infodata['status']:
            url = "https://uc.chaoxing.com/mobileSet/getAppInfo"
            data = {
                'id': 85387,
                'mAppId': 5298819,
                'roleId': infodata['roleId'],
                'deptId': infodata['deptId'],
                'fid': infodata['fid'],
                'time': infodata['time'],
                'enc': infodata['enc'],
            }
            # print(data)
            r = self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
            appInfo = json.loads(r.text)
            if appInfo['status']:
                enc_url = appInfo['info']['pcUrl']
                enc_middle = parse.urlparse(enc_url)
                querys = parse.parse_qs(enc_middle.query)
                enc_finnal = querys['enc'][0]
                # print(appInfo)
                url = "https://office.chaoxing.com/data/apps/forms/fore/commit/types/count"
                data = {
                    'formId': 14673,
                    'formAppId': '',
                    'deptId': infodata['fid'],
                    'limitType': 2,
                    'enc': enc_finnal
                }
                r = self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
                count = json.loads(r.text)
                if count['success']:
                    if count['data']['count'] > 0:
                        return "已填寫過1次",
                    url = "https://office.chaoxing.com/front/web/apps/forms/fore/apply"
                    fidEnc_url = appInfo['info']['openAddr']
                    fidEnc_url = parse.unquote(fidEnc_url)
                    fidEnc_middle = parse.urlparse(fidEnc_url)
                    querys = parse.parse_qs(fidEnc_middle.query)
                    fidEnc_finnal = querys['fidEnc'][0]
                    data = {
                        'uid': self.cookie['_uid'],
                        'code': 'AOvlL0UC',
                        'mappId': 5298819,
                        'appId': appInfo['info']['appId'],
                        'appKey': appInfo['info']['appKey'],
                        'id': appInfo['info']['formId'],
                        'enc': enc_finnal,
                        'state': appInfo['info']['fid'],
                        'formAppId': '',
                        'fidEnc': fidEnc_finnal,
                    }
                    r = self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
                    checkCode = re.findall(r'(?<=checkCode = \')[A-Za-z\d]{32}(?=\',)', r.text)[0]
                    # print(checkCode)
                    url = "https://office.chaoxing.com/data/apps/forms/fore/user/form/verify"
                    data = {
                        'formId': 14673,
                        'formAppId': '',
                        'version': 3,
                        'ext': '',
                        'formData': json.dumps(self.form_data),
                        'uniqueCondition': [],
                        't': 1,
                        'enc': enc_finnal
                    }
                    # print(self.form_data)
                    r = self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
                    res = json.loads(r.text)
                    if not res['success']:
                        return "表單校驗錯誤", res, self.form_data
                    url = "https://office.chaoxing.com/data/apps/forms/fore/user/save?lookuid=" + self.cookie['_uid']
                    data = {
                        'formId': 14673,
                        'formAppId': '',
                        'version': 3,
                        'ext': '',
                        'formData': json.dumps(self.form_data),
                        'uniqueCondition': [],
                        't': 1,
                        'enc': enc_finnal,
                        'checkCode': checkCode,
                        'gatherId': 0,
                        'anonymous': 0,
                        'gverify': '',
                    }
                    r = self.session.post(url, headers=self.headers, data=data, cookies=self.cookie)
                    res = json.loads(r.text)
                    if res['success']:
                        return 0
                    else:
                        return "最終填報失敗", res, self.form_data
                else:
                    return "獲取已填寫次數錯誤", count
            else:
                return "appInfo錯誤", appInfo
        else:
            return "InfoData錯誤", infodata

    def sandImage(self):
        self.session = requests.session()
        url = "https://office.chaoxing.com/data/filedata/get/user/token"
        r = self.session.post(url, headers=self.headers, cookies=self.cookie)
        tokendata = json.loads(r.text)
        # print(tokendata)
        if tokendata['success']:
            token = tokendata['data']['token']
            url = "https://pan-yz.chaoxing.com/upload"
            # print(self.tmp_path)
            file_name = "health_code.jpg"
            # time.sleep(5)
            fb = open("/tmp/" + file_name, 'rb')
            # time.sleep(1)
            files = {'file': (file_name, fb, "image/jpeg")}
            datas = {'puid': self.cookie['_uid'], '_token': token}
            r = self.session.post(url, headers=self.headers, files=files, cookies=self.cookie, data=datas)
            self.health_code = json.loads(r.text)
            file_name = "data_code.jpg"
            fb = open("/tmp/" + file_name, 'rb')
            # time.sleep(1)
            files = {'file': (file_name, fb, "image/jpeg")}
            r = self.session.post(url, headers=self.headers, files=files, cookies=self.cookie, data=datas)
            self.data_code = json.loads(r.text)
            # print(self.data_code,self.health_code)
            if self.data_code['msg'] == 'success' and self.health_code['msg'] == 'success':
                return 0
            else:
                return 2
        return 1


if __name__ == "__main__":
    # 下面改成你的郵箱
    sender = Send(rece="12345678@qq.com")
    try:
        tmp_obj = spawn_fake_image()
        tmp_obj.draw()
        tmp_obj.spawn()
        with open("account.json", encoding="utf-8") as f:
            account_data = json.load(f)
        for i in account_data:
            username = i['username']
            password = i['password']
            info = i['information']
            print("[INFO]" + "用戶名:" + username + "開始打卡")
            break_flag = 0
            for j in range(10):
                if break_flag == 1:
                    break
                if j > 0:
                    time.sleep(1)
                    print("正在重試" + str(j) + "次")
                request1 = req(username, password, name=info['name'], num=info['number'], college=info['college'],
                               education=info['education'], grade=info['grade'])
                login_flag = request1.login()
                if login_flag != 0:
                    msg = "錯誤模塊:登錄\n返回信息:\n" + str(login_flag)
                    print("[ERROR]" + "用戶名:" + username + "打卡失敗\n" + "打卡信息:" + msg)
                    if j < 9:
                        continue
                    sender.title = "打卡錯誤:" + username
                    sender.uid = msg
                    sender.readhtml()
                    sender.sendEmail()
                    continue
                image_sand_flag = request1.sandImage()
                if image_sand_flag != 0:
                    if image_sand_flag == 1:
                        msg = "錯誤模塊:圖片上傳\n返回信息:Token獲取錯誤"
                        print("[ERROR]" + "用戶名:" + username + "打卡失敗\n" + "打卡信息:" + msg)
                        if j < 9:
                            continue
                        sender.title = "打卡錯誤:" + username
                        sender.uid = msg
                        sender.readhtml()
                        sender.sendEmail()
                        continue
                    if image_sand_flag == 2:
                        msg = "錯誤模塊:圖片上傳\n返回信息:上傳錯誤"
                        print("[ERROR]" + "用戶名:" + username + "打卡失敗\n" + "打卡信息:" + msg)
                        if j < 9:
                            continue
                        sender.title = "打卡錯誤:" + username
                        sender.uid = msg
                        sender.readhtml()
                        sender.sendEmail()
                        continue

                request1.make_form()
                sand_flag = request1.sand()
                if sand_flag != 0:
                    if len(sand_flag) == 1:
                        msg = "錯誤模塊:發送\n錯誤問題:" + sand_flag[0]
                        print("[WARNING]" + "用戶名:" + username + "打卡失敗\n" + "打卡信息:" + msg)
                        sender.title = "打卡錯誤:" + username
                        sender.uid = msg
                        sender.readhtml()
                        sender.sendEmail()
                        break_flag = 1
                        break
                    if len(sand_flag) == 2:
                        msg = "錯誤模塊:發送\n錯誤問題:" + sand_flag[0] + "\n返回信息:\n" + sand_flag[1]
                        print("[ERROR]" + "用戶名:" + username + "打卡失敗\n" + "打卡信息:" + msg)
                        if j < 9:
                            continue
                        sender.title = "打卡錯誤:" + username
                        sender.uid = msg
                        sender.readhtml()
                        sender.sendEmail()
                        continue
                    if len(sand_flag) == 3:
                        msg = "錯誤模塊:發送\n錯誤問題:" + sand_flag[0] + "\n返回信息:\n" + sand_flag[1] + "\nData信息\n" + sand_flag[2]
                        print("[ERROR]" + "用戶名:" + username + "打卡失敗\n打卡信息:" + msg)
                        if j < 9:
                            continue
                        sender.title = "打卡錯誤:" + username
                        sender.uid = msg
                        sender.readhtml()
                        sender.sendEmail()
                        continue
                # print(login_flag,image_sand_flag,sand_flag)
                if login_flag == 0 and image_sand_flag == 0 and sand_flag == 0:
                    print("[INFO]" + "用戶名:" + username + "打卡成功")
                    sender.title = "打卡成功:" + username
                    sender.uid = "賬號" + username + "已完成自動打卡"
                    sender.readhtml()
                    sender.sendEmail()
                    break_flag = 1
                    break
            time.sleep(1)
    except Exception as e:
        print(e)
        sender.title = "打卡錯誤"
        sender.uid = e
        sender.readhtml()
        sender.sendEmail()
