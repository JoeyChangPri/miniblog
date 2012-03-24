# -*- coding:utf-8 -*-

import web
from web.template import render_mako

class BaseHandler(object):

    def __init__(self):
        self.ctx = web.ctx
        self.render = render
        self.ip = web.ctx['env'].get("HTTP_X_FORWARDED_FOR", "127.0.0.1")


render = render_mako(directories=[PROJECT_PATH + '/templates'],
                     default_filters=['decode.utf_8'],
                     input_encoding='utf-8',
                     output_encoding='utf-8',
                     module_directory = PROJECT_PATH + '/tmp',
                     encoding_errors = 'replace')
