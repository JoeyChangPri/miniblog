#! usr/bin/evn python
# -*- coding:utf-8 -*-
'''
Author: Chang.Jian
Contact: changjian53@gmail.com
'''
import datetime
import sys

sys.path.append('/home/cj/changjian/miniblog/')

import pymongo

import settings


def main():
    con = pymongo.Connection("mongodb://%s:%s" % (settings.DBHOST, settings.DBPORT))
    col = con['miniblog']['artical']
    artical = dict(id=1, 
                   tags='',
                   title='留言板',
                   author='Chang.Jian',
                   content='',
                   category_id=1,
                   times=1000,
                   update=datetime.date.today().isoformat(),
                   uptime=datetime.datetime.now(),
                   instime=datetime.datetime.now(),
                   insdate=datetime.date.today().isoformat(),
                   status=True)
    col.insert(artical)
    con.disconnect()

if  __name__ == '__main__':
    main()
    print 'Done'