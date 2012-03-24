#coding:utf-8
import os
import time
import urllib

import web

import settings
from utils.baserender import render
from utils.mongodb import get_col_handler

def render_to_response(tmpname, context={}):
    return getattr(render, tmpname)(**context)

def import_modules(apps):
    urls = []
    for appname in apps:
        app = __import__(appname, {}, {}, ["urls"])
        flag = False
        for url in app.urls.urls:
            if flag:
                url = "%s.%s" %(appname, url)
            urls.append(url)
            flag = not flag
        
    return urls

def smart_str(s, encoding='utf-8'):
    """
    返回编码后的字符串
    """
    if isinstance(s, unicode):
        return s.encode(encoding)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8').encode(encoding)
    else:
        return s
    

 
def switch_time_zone():
    """
    切换时区到settings.TIME_ZONE
    """
    os.environ["TZ"] = settings.TIME_ZONE
    time.tzset()
    
def flush_tags():
    """
    刷新文章标签，每次写一篇文章后，刷新标签
    """
    artical_handler = get_col_handler('artical')
    articals  = artical_handler.find({'status':True})
    tags = set([])
    for artical in articals:
        [tags.add(urllib.quote(smart_str(i))) for i in artical['tags'].split(' ') if i.strip()]
    
    tags_file = open(settings.PROJECT_PATH + '/templates/tags.html', 'w')
    content = render_to_response('tags_tmp', {'tags':tags})
    tags_file.write(content)
    tags_file.close()
    
def send_email(recipients, subject, messages):
    msg_header = u'您好:\n\t您在常剑的博客中的留言，得到回复。内容如下:\n\t'
    messages = msg_header + messages
    web.sendmail('changjian53@gmail.com', recipients, subject, messages)

