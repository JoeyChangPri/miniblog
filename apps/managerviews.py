#coding:utf-8

import pymongo
import web
from web import form as _
from apps.basehandler import BaseHandler
from apps.collections import Category, Link, Artical, Comment
from apps.forms import cgform, articalf, linkform
from apps.apputils import get_comments_in_comment
#from utils.baseutils import smart_str
from utils.baseutils import render_to_response
from utils.baseauth import authenticate_admin

class index(BaseHandler):
    
    def GET(self):
#        render = render_mako(directories=['templates'],
#                    input_encoding='utf-8',
#                    output_encoding='utf-8',
#                    module_directory = '/tmp/miniblog/mako_modules',
#                    encoding_errors = 'replace',
#                    format_exceptions = True,)        
        return self.render.manager_index()
    
class cgshow(BaseHandler):
    """
    show and add categories
    """    
    def GET(self):
        col_handler = self.col_handler('category')
        artical_handler = self.col_handler('artical')
        objs = col_handler.find().sort('id', pymongo.DESCENDING)
        form = cgform()
        return render_to_response('category/manager_category', 
                                  {'form':form, 
                                   'objs':objs,})
    
    def POST(self):
        col_handler = self.col_handler('category')
        objs = col_handler.find().sort('id', pymongo.DESCENDING)
        form = cgform()
        if not form.validates():
            return render_to_response('category/manager_category', {
                'form':form,
                'objs':objs,
            })
        categroy = Category(form['name'].get_value())
        info = categroy.save()
        return web.seeother('/manager/category')
    
class cgdel(BaseHandler):
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        id = int(id)
        col_handler = self.col_handler('category')
        artical_handler = self.col_handler('artical')
        result = artical_handler.find_one({'category_id':id})
        if result:
            return "<script>alert('Can not remove this category!There are some\
articals');window.location.href='/manager/category';</script>"
#        col_handler.remove({'id':int(id)})
        return "<script>alert('Deleted!');window.location.href='/manager/category';</script>"
    
class cgedit(BaseHandler):
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        col_handler = self.col_handler('category')
        id = int(id)
        category = col_handler.find_one({'id':id})
        form = cgform()
        form.fill({'id':id, 'name':category['name']})
        fancybox = False
        return render_to_response('category/manager_catedit', {'form':form, 
            'fancybox':fancybox,
        })
    
    def POST(self, id):
        form = cgform()
        if not form.validates():
            return render_to_response('category/manager_catedit', {
                'form':form,
                'fancybox':False
            })
        categroy = Category(form['name'].get_value(), id=int(id))
        info = categroy.save()
        fancybox = True
        return render_to_response('category/manager_catedit', {'form':form, 
            'fancybox':fancybox,
            })            
            
class artical(BaseHandler):
    """
    显示所有文章
    """
    def GET(self):
        artical_handler = self.col_handler('artical')
        comment_handler = self.col_handler('comment')
        objs = artical_handler.find().sort('id', pymongo.DESCENDING)
        articals = []
        for obj in objs:
            sum = comment_handler.find({'artical_id':obj['id']}).count()
            articals.append([obj, sum])
        return render_to_response('artical/manager_artical', {'articals':articals})
    
class articaladd(BaseHandler):
    """
    添加文章
    """
    def GET(self):
        col_handler = self.col_handler('artical')
        form = articalf()   
        form.inputs = (_.Dropdown("category_id", 
        args=map(lambda i:(i['id'], i['name']), self.col_handler('category').find()), 
        description="Category"),) + form.inputs
        return render_to_response('artical/manager_add_artical', {'form':form})
    
    def POST(self):
        col_handler = self.col_handler('artical')    
        form = articalf()
        form.inputs = (_.Dropdown("category_id", 
                args=map(lambda i:(i['id'], i['name']), self.col_handler('category').find()), 
                description="Category"),) + form.inputs        
        if not form.validates():
            return render_to_response('artical/manager_add_artical', {'form':form})
        artical = Artical(
            form['title'].get_value(),
            form['tags'].get_value(),
            form['content'].get_value(),
            form['category_id'].get_value(),
            form['author'].get_value(),
            id=form['id'].get_value()
            )
        artical.save()
        return web.seeother('/manager/artical')
 
class articaledit(BaseHandler):
    """编辑文章
    """
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        id = int(id)
        col_handler = self.col_handler('artical')
        artical = col_handler.find_one({'id':id})
        form = articalf()   
        form.inputs = (_.Dropdown("category_id", 
        args=map(lambda i:(i['id'], i['name']), self.col_handler('category').find()), 
        description="Category"),) + form.inputs        
        form.fill({'id':id, 'category_id':artical['category_id'],
                   'content':artical['content'], 
                   'title':artical['title'],
                   'tags':artical['tags'],
                   'author':artical['author'],
                   })
        
        return render_to_response('artical/manager_add_artical', {'form':form})
        
    def POST(self, id):
        col_handler = self.col_handler('artical')    
        form = articalf()
        form.inputs = (_.Dropdown("category_id", 
                args=map(lambda i:(i['id'], i['name']), self.col_handler('category').find()), 
                description="Category"),) + form.inputs        
        if not form.validates():
            return render_to_response('artical/manager_add_artical', {'form':form})
        artical = Artical(
            form['title'].get_value(),
            form['tags'].get_value(),
            form['content'].get_value(),
            form['category_id'].get_value(),
            form['author'].get_value(),
            id=form['id'].get_value()
            )
        artical.save()
        return web.seeother('/manager/artical')        
 
class articaldel(BaseHandler):
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        col_handler = self.col_handler('artical')
        col_handler.remove({'id':int(id)})
        return "<script>alert('Deleted!');window.location.href='/manager/artical';</script>"

class comment(BaseHandler):
    """首先显示文章，点击文章进入和首页显示类似的页面。但是操作不同，提供删除,原本是提供回复
    """
    
    def GET(self):
        artical_handler = self.col_handler('artical')
        comment_handler = self.col_handler('comment')
        objs = artical_handler.find({'id':{'$ne':1}}).sort('id', pymongo.DESCENDING)
        articals = []
        for obj in objs:
            sum = comment_handler.find({'artical_id':obj['id']}).count()
            articals.append([obj, sum])
        return render_to_response('comment/manager_pre_comment', {'articals':articals})    
        
class commentshow(BaseHandler):
    """显示具体文章的评论
    """
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        id = int(id)
        comment_children = []
        
        artical_handler = self.col_handler('artical')
        comment_handler = self.col_handler('comment')
        
        comments = comment_handler.find({'artical_id':id})
        if comments.count():
            for comment in comments:
                children = get_comments_in_comment(comment['id'])
                comment_children.append([comment, children])
        artical = artical_handler.find_one({'id':id})   
        
        return render_to_response('comment/manager_comment_show', {
                                  'artical':artical,
                                  'comment_children':comment_children,
                                  })
        

class commentdel(BaseHandler):
    """删除评论->改变状态"""
    
    def GET(self, aid, cid):
        if not (aid.isdigit() and cid.isdigit()):
            return "ID is Wrong!"
        aid = int(aid)
        cid = int(cid)
        
        comment_handler = self.col_handler('comment')
        comment = comment_handler.find_one({'id':cid})
        comment_handler.remove({'id':cid})

        return """<script>alert('Deleted!');window.location.href=
'/manager/comment_show/%s';</script>""" % aid


class link(BaseHandler):
    """
    友情链接
    """
    def GET(self):
        col_handler = self.col_handler('link')
        objs = col_handler.find().sort('id', pymongo.DESCENDING)
        form = linkform()
        return render_to_response('category/manager_link', {'form':form, 'objs':objs})
    
    def POST(self):
        col_handler = self.col_handler('link')
        objs = col_handler.find().sort('id', pymongo.DESCENDING)
        form = linkform()
        if not form.validates():
            return render_to_response('category/manager_link', {
                'form':form,
                'objs':objs,
            })
        link = Link(form['link_addr'].get_value(), 
            form['link_name'].get_value(),
            form['friend_name'].get_value(),
            form['description'].get_value() 
        )
#        print 'aa'
        info = link.save()
        return web.seeother('/manager/link')    
    
class linkdel(BaseHandler):
    
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        col_handler = self.col_handler('link')
        col_handler.remove({'id':int(id)})
        return "<script>alert('Deleted!');window.location.href='/manager/link';</script>"

class linkedit(BaseHandler):
    """
    友情链接编辑
    """
    def GET(self, id):
        if not id.isdigit():
            return "ID is Wrong!"
        col_handler = self.col_handler('link')
        id = int(id)
        link = col_handler.find_one({'id':id})
        form = linkform()
        form.fill({'id':id, 
            'link_name':link['link_name'], 
            'link_addr':link['link_addr'],
            'friend_name':link['friend_name'],
            'description':link['description'],
            })
#        form = cgform()
        fancybox = False
        return render_to_response('category/manager_linkedit', {'form':form, 
            'fancybox':fancybox,
        })
    
    def POST(self, id):
        form = linkform()
        if not form.validates():
            return render_to_response('category/manager_linkedit', {
                'form':form,
                'fancybox':False,
            })
        link = Link(form['link_addr'].get_value(), 
            form['link_name'].get_value(),
            form['friend_name'].get_value(),
            form['description'].get_value(),
            id=int(id))
        info = link.save()
        fancybox = True
        return render_to_response('category/manager_linkedit', {'form':form, 
            'fancybox':fancybox,
            })            
            
class Login(BaseHandler):
    """
    登录
    """
    
    def GET(self):
        return render_to_response("admin/login")
    
    def POST(self):
        args = web.input(name="", password="")
        if authenticate_admin(args.name, args.password):
            web.config._session['logged_in'] = True
            raise web.seeother("/manager/index")
        raise web.seeother("/manager/login")
    
class Logout(BaseHandler):
    """
    注销
    """
    
    def GET(self):
        web.config._session.logged_in = False
        raise web.seeother("/manager/login")
