#coding:utf-8
import sys

import web
from utils.baseutils import import_modules, switch_time_zone
from utils.baseauth import admin_auth
from db_init import db_init

APPS = ("apps",)

web.config.debug = False
#configure the mail settings
web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = '***********'
web.config.smtp_password = '********'
web.config.smtp_starttls = True

app = web.application(import_modules(APPS), autoreload=False)

session = web.session.Session(app, web.session.DiskStore('sessions'))
web.config._session = session

app.add_processor(web.loadhook(admin_auth))


if __name__ == '__main__':
    switch_time_zone()
    db_init()
    if "deploy" in sys.argv:
        from flup.server.fcgi import WSGIServer
        func = app.wsgifunc()
        server_address = '/tmp/miniblog.sock'
        WSGIServer(
            func,
            bindAddress=server_address,
            maxSpare=16,
            minSpare=16,
#            maxRequests=128,
#            maxChildren=32
        ).run()
    else:
        app.run()
