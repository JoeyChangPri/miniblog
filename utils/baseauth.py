# -*- coding:utf-8 -*-

import web
import settings

def authenticate_admin(user='', password=''):
    """
    验证是否一致
    """
    return settings.USER == user and settings.PASSWORD == password

def admin_auth():
    """
    判断session是否过期
    """
    
    path = web.ctx.path
    if path.startswith("/manager/") \
                and not path == "/manager/login" \
                and not web.config._session.get("logged_in", False):
        raise web.seeother("/manager/login")    