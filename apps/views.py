#coding:utf-8
import urllib
import pickle

import web
import pymongo


from apps.basehandler import BaseHandler
from apps.apputils import get_left_objs, get_comments_in_comment
from utils.mongodb import get_col_handler
from utils.baseutils import smart_str
from utils.baseutils import send_email
from utils.paginator import Paginator
from forms import commentf
from apps.collections import Comment

COOKIE_NAME = 'cj53.com'

class blog(BaseHandler):
    
    def GET(self):
        args = web.input(page='1')
        if not args.page.isdigit():
            return web.notfound()
        page = int(args.page)
        per_page = 7
        artical_handler = get_col_handler('artical')
        total = artical_handler.find({'id':{'$ne':1}}).sort('uptime', \
        pymongo.DESCENDING).count()        
        
        paginator = Paginator(total, page, per_page=per_page)
        pre_articals, pre_links, pre_comments, pre_categories = get_left_objs()
        articals = artical_handler.find({'id':{'$ne':1}}).sort('uptime', \
pymongo.DESCENDING).limit(per_page).skip((page-1)*per_page)
        return self.render.index(
            pre_articals=pre_articals, 
            pre_links=pre_links,
            pre_comments=pre_comments,
            pre_categories=pre_categories,
            articals=articals, 
            paginator=paginator, 
            tip='')
    
class artical(BaseHandler):
    
    def GET(self, id=1):
        pre_articals, pre_links, pre_comments, pre_categories= get_left_objs()
        id = int(id)
        comment_children = []
        
        artical_handler = get_col_handler('artical')
        comment_handler = get_col_handler('comment')
        comments = comment_handler.find({'artical_id':id})
        if comments.count():
            for comment in comments:
                children = get_comments_in_comment(comment['id'])
                comment_children.append([comment, children])
        artical = artical_handler.find_one({'id':id})
        form = commentf()
        
        
        cookie = web.cookies().get(COOKIE_NAME, None)
        name = email = website = ''
        if cookie:
            cookie = pickle.loads(cookie)
            name = urllib.unquote(cookie.get('name', ''))
            email = cookie.get('email', '')
            website = cookie.get('website', '')
        
        form.fill({'artical_id':int(id), 
                   'id':0, 
                   'comment_id':0,
                   'name':name,
                   'email':email,
                   'website':website})
        if not artical:
            return "<script>alert('别乱点!');window.location.href='/';</script>"
        return self.render.artical_detail(pre_articals=pre_articals,
                                          pre_links=pre_links, 
                                          pre_comments=pre_comments,
                                          pre_categories=pre_categories,
                                          artical=artical,
                                          form=form, 
                                          comments=comment_children)
    
    def POST(self, id=1):
        pre_articals, pre_links, pre_comments, pre_categories = get_left_objs()
        id = int(id)
        comment_children = []
        
        artical_handler = get_col_handler('artical')
        artical = artical_handler.find_one({'id':id})
        comment_handler = get_col_handler('comment')
        comments = comment_handler.find({'artical_id':id})
        if comments.count():
            for comment in comments:
                children = get_comments_in_comment(comment['id'])
                comment_children.append([comment, children])        
        form = commentf()
        if not form.validates():
            return self.render.artical_detail(pre_articals=pre_articals,
                                              pre_links=pre_links, 
                                              pre_comments=pre_comments,
                                              pre_categories=pre_categories,
                                              artical=artical,
                                              form=form, 
                                              comments=comment_children)
        check = web.input().get('remember_me', 'false')
        artical_id = web.input().get('artical_id', 1)
        name = web.input().get('name', '')
        email = web.input().get('email', '')
        website = web.input().get('website', '')
        content = web.input().get('content', '')
        comment_id = web.input().get('comment_id', 0)
        
        params = dict(name=urllib.quote(smart_str(name)), email=email, website=website)
        cookie_value = pickle.dumps(params)
        if check == 'false':
            pass
        else:
            web.setcookie(COOKIE_NAME, cookie_value, expires=2592000)
        comment = Comment(artical_id,
                          name,
                          email,
                          website,
                          content,
                          comment_id)
        comment.save()
        # TODO:Package this part
        comment_obj = comment_handler.find_one({'id':int(comment_id)})
        if int(comment_id) != 0:
#            comment_obj = comment_handler.find_one({'id':int(comment_id)})
            send_email(comment_obj.get('email', ''), u'来自%s的回复' % name, \
u'%s\n详情请看:http://www.cj53.com/click/%s' % (content, artical_id))
        send_email('272171075@qq.com', u'有留言', \
u'%s\n详情请看:http://www.cj53.com/click/%s' % (content, artical_id))        
        if id == 1:
            raise web.seeother("/board")
        return web.seeother("/artical/%s" % id)
    
board = artical

class category(BaseHandler):
    """按分类获取文章
    """
    
    def GET(self, id=0):
        args = web.input(page='1')
        id = int(id)
        articals = None
        artical_handler = self.col_handler('artical')
        category_handler = self.col_handler('category')
        category = category_handler.find_one({'id':id})
        tip = "分类:%s" % smart_str(category['name'])
        per_page = 7
        if not args.page.isdigit() or id==1:
            return web.notfound()
        page = int(args.page) 
        conditions = {'status':True, 'id':{'$ne':1}}
        if id > 1:
            conditions.update(category_id=id)
        total = artical_handler.find(conditions).count()
        paginator = Paginator(total, page, per_page=per_page)
        articals = artical_handler.find(conditions).sort('uptime', \
pymongo.DESCENDING).limit(per_page).skip((page-1)*per_page)
        
        pre_articals, pre_links, pre_comments, pre_categories = get_left_objs()
        
        return self.render.index(pre_articals=pre_articals, 
                                 pre_links=pre_links,
                                 pre_comments=pre_comments,
                                 pre_categories=pre_categories,
                                 articals=articals,
                                 paginator=paginator, 
                                 tip=tip)
  

class tags(BaseHandler):
    
    def GET(self):
        tag = web.input(tag='').get('tag', '')
        tag = smart_str(urllib.unquote(tag))
        artical_handler = self.col_handler('artical')
        tip = "标签:%s" % tag
        if not tag:
            return web.notfound()
        articals = artical_handler.find({'tags':{'$regex':tag}, 'status':True})\
.sort('uptime', pymongo.DESCENDING)
        pre_articals, pre_links, pre_comments, pre_categories = get_left_objs()
        return self.render.index_tags(pre_articals=pre_articals, 
                                 pre_links=pre_links,
                                 pre_comments=pre_comments,
                                 pre_categories=pre_categories,
                                 articals=articals,
                                 tip=tip)        
        
class click(BaseHandler):
    """
    统计次数,简单的跳转。防止刷新的时候重复统计
    """
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        id = int(id)
        if id == 1:
            raise web.seeother('/board')
        artical_handler = self.col_handler('artical')
        try:
            result = artical_handler.database.eval("""db.artical.findAndModify
({update:{$inc:{times:1}}, query:{id:%s}, new:true})""" % id)
        except Exception, e:
            print e
            return web.notfound()
        raise web.seeother('/artical/%s' % id)
