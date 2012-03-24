#coding:utf-8

import settings
from utils.mongodb import get_col_handler

col_name = 'ids'
col_handler = get_col_handler(col_name)

def db_init():
    for col in settings.COLLECTIONS:
        if col_handler.find_one({'name':col}):
            pass
        else:
            col_handler.insert({'name':col, 'id':0})
            this_col_handler = get_col_handler(col)
            this_col_handler.create_index('id')
