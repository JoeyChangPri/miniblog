#coding:utf-8
"""
觉得这个有点多余，当作是用来判断字段内容的合法性吧
"""
import datetime

from utils.mongodb import get_col_handler
from utils.baseutils import smart_str, flush_tags

class Collection(object):
    """
    基类collection (字典类型)
    """
    def __init__(self, *args, **kwargs):
        self.fields.update(kwargs)
        
    def save(self):
        col = self.__class__.__name__.lower()
        get_col_handler(col).save(self.fields)
        return "OK"        
        
    def remove(self):
        col = self.__class__.__name__.lower()
        get_col_handler(col).remove(self.fields)
    
    
class Category(Collection):
    """文章分类表"""
    def __init__(self, name, id=0):
        self.name = smart_str(name)
        self.id = int(id)
        self.fields = {'name':self.name}
        if self.id != 0:
            self.fields.update(id=self.id)
        
        
        
    def save(self):
        col = self.__class__.__name__.lower()
        get_col_handler(col).save(self.fields)
        return "OK"   
    
    
class Artical(Collection):
    """文章"""
    def __init__(self, 
        title, 
        tags, 
        content, 
        category_id, 
        author,
        times = 0,
        status=True, 
        id=0):
        self.fields = {}
        self.id = int(id)
        self.fields.update(title=smart_str(title), 
            tags=smart_str(tags),
            content=smart_str(content),
            category_id=int(category_id),
            author=smart_str(author),
            times=times,
            update=datetime.date.today().isoformat(),
            uptime=datetime.datetime.now(),
            instime=datetime.datetime.now(),
            insdate=datetime.date.today().isoformat(),
            status=status)
        if self.id != 0:
            self.fields.update(id=self.id)
    
    def save(self):
        col = self.__class__.__name__.lower()
        if self.id != 0:
            col_handler = get_col_handler(col)
            artical = col_handler.find_one({'id':self.id})
            self.fields['times'] = artical['times']
            self.fields['instime'] = artical['instime']
            self.fields['insdate'] = artical['insdate']
            self.fields['update'] = datetime.date.today().isoformat()
            self.fields['uptime'] = datetime.datetime.now()
        get_col_handler(col).save(self.fields)
        flush_tags()
        return "OK"    


class Comment(Collection):
    """评论"""
    def __init__(self, artical_id, name, email, website, content, comment_id=0, 
                 status=True, id=0):
        self.fields = {}
        self.id = int(id)
        self.fields.update(artical_id=int(artical_id),
                           name=smart_str(name), 
                           email=smart_str(email),
                           website=smart_str(website),
                           content=smart_str(content),
                           comment_id=int(comment_id),
                           instime=datetime.datetime.now(),
                           status=status)
        if id != 0:
            self.fields.update(id=self.id)
        
                
class Link(Collection):
    """友情链接"""
    def __init__(self, link_addr, link_name, friend_name, description="",
        insdate=datetime.datetime.today(),status=True, id=0):
        self.fields = {}
        self.id = int(id)
        self.fields.update(link_addr=link_addr,
            link_name=smart_str(link_name),
            friend_name=smart_str(friend_name),
            description=smart_str(description),
            insdate=insdate,
            status=status)
        if self.id != 0:
            self.fields.update(id=self.id)
            
#class User(Collection):
#    """用户"""
#    def __init__(self, name, email, status=True, id=0):
#        self.fields.update(name=name,
#            email=email,
#            status=status)
#        if id != 0:
#            self.fields.update(id=int(id))