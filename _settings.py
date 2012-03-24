#coding:utf-8

import os
#config database


#db = web.database(dbn=dbn, user=user, pw=pw, db=db)
#DB config
DBHOST = ''   			# add your mongodb host
DBPORT = 00000  		# add your mongodb port
DBNAME = 'miniblog'   	# add your collection name
DBUSER = ''    			# add your username
DBPSK = ''				# add your password

COLLECTIONS = (
    'category',
    'artical',
    'comment',
    'link',
    'user'
)


USER = '**'				# 后台用户名
PASSWORD = '**'			# 后台用户密码

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

TIME_ZONE = "Asia/Shanghai"