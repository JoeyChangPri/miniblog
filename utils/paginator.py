# -*- coding:utf-8 -*-
"""
根据总数生成Paginator对象
"""

import math

class Paginator(object):

    def __init__(self, total, page, per_page=10, page_range=5):
        try:
            self.total = int(total)
            self.total_ = int(total)
            self.per_page = int(per_page)
            self.page_range = int(page_range)
        except:
            raise ValueError("must be digit")
        self.total = self.total or 1
        self.maxpage = self.get_maxpage()
        try:
            self.page = int(page)
        except:
            self.page = 1
        if not (self.page >= 1 and self.page <= self.maxpage):
            self.page = 1
        self.offset = ( self.page - 1 ) * per_page

    def get_maxpage(self):
        return int(math.ceil(float(self.total)/self.per_page))

    def get_pagerange(self):
        """
        生成合适的pagerange
        """
        page_range = [x for x in range(self.page-self.page_range, self.page+self.page_range)]
        toadd = max((1 - page_range[0]), 0)
        page_range = [x + toadd for x in page_range]
            
        tosub = max((page_range[-1] - self.maxpage), 0)
        page_range = [x - tosub for x in page_range]
        page_range = [x for x in page_range if x > 0 and x <= self.maxpage]
            
        if 1 not in page_range:
            page_range = ([1, 0] if min(page_range) > 2 else [1]) + page_range
        if self.maxpage not in page_range:
            page_range += ([0, self.maxpage] if (max(page_range) < self.maxpage - 1) else [self.maxpage])
        return page_range

    def get_full_pagerange(self):
        return range(1, self.maxpage+1)

    def has_next(self):
        return self.page != self.maxpage

    def has_previous(self):
        return self.page != 1
    
    def get_pretty_display(self, other=""):
        ret = ""
        if self.has_previous():
            ret += u'''<a class="page_number" href="?%spage=%s">上一页</a>''' % (other, self.page-1)
        for _page in self.get_pagerange():
            if _page == 0:
                ret += u'''...'''
            elif _page == self.page:
                ret += u'''<span class="current_page">%s</span>''' % _page
            else:
                ret += u'''<a class="page_number" href="?%spage=%s">%s</a>''' % (other, _page, _page)
        if self.has_next():
            ret += u'''<a class="page_number" href="?%spage=%s">下一页</a> ''' % (other, self.page+1)
        return ret
        
        
