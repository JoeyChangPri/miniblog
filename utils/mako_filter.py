# -*- coding:utf-8 -*-

from utils.mongodb import get_col_handler

def count_artical_by_category(id):
    """根据category id计算该category下的文章数量,不包括删除的文章
    """
    try:
        id = int(id)
    
        artical_handler = get_col_handler('artical')
        sum = artical_handler.find({'status':True, 'category_id':id}).count()
        return sum
    except:
        return 0

def get_category_name(id):
    """根据artical_id找到category
    """
    try:
        id = int(id)
        
        artical_handler = get_col_handler('artical')
        category_handler = get_col_handler('category')
        category_id = artical_handler.find_one({'id':id})['category_id']
        name = category_handler.find_one({'id':category_id})['name']
        
        return name
    except:
        return 'Unknown'

def count_comment_by_artical(id):
    """根据artical id计算评论数量,包括删除的评论
    """
    try:
        id = int(id)
    
        comment_handler = get_col_handler('comment')
        sum = comment_handler.find({'artical_id':id}).count()
        return sum
    except:
        return 0