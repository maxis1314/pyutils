# coding: utf-8


_DBUSER = "root" # 数据库用户名
_DBPASS = "" # 数据库密码
_DBHOST = "localhost" # 数据库地址
_DBNAME = "flaskblog" # 数据库名称

#config
SECRET_KEY = 'flaskblog'
BLOG_TITLE = 'My Blog'
BLOG_URL = 'http://localhost:5000/'
BLOG_NAME = 'Blog'

#admin info
ADMIN_INFO = ''
ADMIN_EMAIL = ''
ADMIN_USERNAME = 'ADMIN'

class rec: pass

rec.database = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST,_DBNAME)
rec.description = u"my blog"
rec.url = 'http://localhost:5000/'
rec.paged = 8
rec.archive_paged = 20
rec.admin_username = 'admin'
rec.admin_email = ''
rec.admin_password = '1'
rec.default_timezone = "Asia/Shanghai"
