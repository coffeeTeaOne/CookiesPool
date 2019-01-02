from ConnDB.db_mysql import Op_Mysql

CODE_ = 'sina'
NAME_ = 'name'
ACCOUNTS_ = []
with open('./config/userpwd.txt', 'r', encoding='utf-8') as f:
    res = f.readlines()
    for i in res:
        user_pwd = i.split(':')
        s_data = '{"user":"' + str(user_pwd[0]) + '","pwd":"' + str(user_pwd[1].replace('\n',''))+'"}'
        ACCOUNTS_.append(eval(s_data))
ACCOUNTS_ = str(ACCOUNTS_)
URL_ = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/'
SCRIPT_ = '''[{
	"id": "1",
	"title": "输入  命令",
	"name": "用户名",
	"type": "input",
	"xpath": "//input[@id='loginName']",
	"algo": "",
	"value": "$U"
}, {
	"id": "2",
	"title": "输入  命令",
	"name": "密码",
	"type": "input",
	"xpath": "//input[@id='loginPassword']",
	"algo": "",
	"value": "$P"
}, {
	"id": "3",
	"title": "点击  命令",
	"name": "第一次登录",
	"type": "click",
	"xpath": "//a[@id='loginAction']",
	"algo": "",
	"value": ""
}, {
	"id": "4",
	"title": "验证码  命令",
	"name": "验证码",
	"type": "algo",
	"xpath": "",
	"algo": "",
	"value": ""
}, {
	"id": "5",
	"title": "提交  命令",
	"name": "登录",
	"type": "commit",
	"xpath": "",
	"algo": "",
	"value": ""
}]'''

STATUS_ = 'DRAFT'
SCHE_TYPE_ = 'DAY'
column = ['CODE_', 'NAME_', 'ACCOUNTS_', 'URL_', 'SCRIPT_', 'STATUS_', 'SCHE_TYPE_']
data = [(CODE_, NAME_, ACCOUNTS_, URL_, SCRIPT_, STATUS_, SCHE_TYPE_)]
Op_Mysql().Insert_Query(tablename='spi_auto_login', column=column, datas=data)
print('完成！')

