import requests
import json
import time
import re


headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}


def login_web():
    login_url = 'https://www.******.com/admin/login.php'
    postdata = {'account': 'web_name',
                'pwd': 'web_password'}
    session = requests.session()
    req = session.post(login_url, data=postdata, headers=headers)
    go_url = 'https://www.******.com/admin/member-list.php'
    req = session.get(go_url, headers=headers)
    if req.status_code == 200 and '會員資料管理' in req.text:
        print('登陆成功')
        member_list()
    else:
        print('登陆失败')


def member_list():
    url = 'https://www.******.com/admin/json-member-list.php'
    p = 0
    time.sleep(1)
    while True:
        p += 1
        post_data = {'page': p,
                     'rp': 30,
                     'sortname': 'uid',
                     'sortorder': 'desc',
                     'query': None,
                     'qtype': 'name'}
        time.sleep(1)
        jsdata = requests.post(url, headers=headers, data=post_data)
        jsdata = jsdata.content
        js_str = jsdata.decode()
        # print(soup_list)
        if len(js_str) == 0:
            continue
        else:
            soup = json.loads(js_str)
            soup_list = str(soup['rows'])
            name = re.findall(r'nam.*?([\u2E80-\u9FFF\s\w\\t]+)./a>', soup_list)
            account = re.findall(r'acco.*?([\w]+@[\w]+\.[\w]+)',soup_list)
            sex = re.findall(r'sex.*?([\u4e00-\u9fff])',soup_list)
            school = re.findall(r'sch.*?([\u4e00-\u9fff]+|\'\')',soup_list)
            password = re.findall(r'password.*?([\w!@#$%^&*]+)',soup_list)
            birthday = re.findall(r'bir.*?([\d]+-[\d]+-[\d]+)',soup_list)
            city = re.findall(r'cit.*?([\u2E80-\u9FFF]+|\'\')',soup_list)
            address = re.findall(r'addr.*?([\w]+[\s]+[\u2E80-\u9FFF\w]+|\'\')',soup_list)
            mobile = re.findall(r'mob.*?([\d]+-[\d]+-[\d]+|\d+)',soup_list)
            if len(soup['rows']) == 0:
                print('当前内容为空')
                break
            for name,account,sex,school,password,birthday,city,address,mobile in zip(name,account,sex,school,password,birthday,city,address,mobile):
                mergers = name+'---'+account+'---'+sex+'---'+school+'---'+password+'---'+birthday+'---'+city+'---'+address+'---'+mobile
                with open('E:\TEST.txt','a',encoding='utf-8') as f:
                    f.write(mergers+'\n')
                print(mergers)



if __name__ == "__main__":
    start = time.time()
    login_web()
    end = time.time()
    print('总耗时: %s ' % (end - start))