#coding:utf-8

urls = (
    '/manager/index', 'managerviews.index',
    '/manager/category', 'managerviews.cgshow',
    '/manager/cate_del/(\d+)', 'managerviews.cgdel',
    '/manager/cate_edit/(\d+)', 'managerviews.cgedit',
    '/manager/artical', 'managerviews.artical',
    '/manager/artical_add', 'managerviews.articaladd',
    '/manager/artical_del/(\d+)', 'managerviews.articaldel',
    '/manager/artical_edit/(\d+)', 'managerviews.articaledit',
    '/manager/link', 'managerviews.link',
    '/manager/link_del/(\d+)', 'managerviews.linkdel',
    '/manager/link_edit/(\d+)', 'managerviews.linkedit',
    '/manager/comment', 'managerviews.comment',
    '/manager/comment_show/(\d+)', 'managerviews.commentshow',
    '/manager/comment_del/(\d+)/(\d+)', 'managerviews.commentdel',
    '/manager/login', 'managerviews.Login',
    '/manager/logout', 'managerviews.Logout',
)

urls += (
    '/', 'views.blog',
    '/artical/(\d+)', 'views.artical',
    '/board', 'views.board',
    '/category/(\d+)', 'views.category',
    '/click/(\d+)', 'views.click',
    '/tags', 'views.tags',
)   
