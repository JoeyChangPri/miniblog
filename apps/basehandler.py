#coding: utf-8
import web

from utils.baserender import render
from utils.mongodb import get_col_handler as _

class BaseHandler(object):
    
    def __init__(self):
        self.ctx = web.ctx
        self.render = render
        self.col_handler = _
        self.ip = web.ctx['env'].get("HTTP_X_FORWARDED_FOR", "127.0.0.1")
