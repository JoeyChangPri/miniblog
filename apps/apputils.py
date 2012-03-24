# -*- coding: utf-8 -*-

import pymongo

from utils.mongodb import get_col_handler

def get_left_objs():
    objs = []
    artical_handler = get_col_handler('artical')
    tmp = artical_handler.find({'id':{'$ne':1}, 'status':True}).sort('uptime', \
pymongo.DESCENDING).limit(7)
    objs.append(tmp)
    link_handler = get_col_handler('link')
    tmp = link_handler.find().sort('instime', pymongo.DESCENDING).limit(7)
    objs.append(tmp)
    commt_handler = get_col_handler('comment')
    tmp = commt_handler.find({'status':True}).sort('id', pymongo.DESCENDING).limit(7)
    objs.append(tmp)
    category_handler = get_col_handler('category')
    tmp = category_handler.find({'id':{'$ne':1}}).sort('id', pymongo.DESCENDING)
    objs.append(tmp)
    return objs

commt_ids = []

def get_comments_in_comment(comment_id):
    global commt_ids
    commt_handler = get_col_handler('comment')
    comment = commt_handler.find_one({'id':int(comment_id)})
    comment_to_id = comment['comment_id'] or 0
    if int(comment_to_id) == 0:
        tmp = commt_ids
        commt_ids = []
        return tmp
    else:
        commt_ids.append(commt_handler.find_one({'id':int(comment_to_id)}))
        return get_comments_in_comment(comment_to_id)
