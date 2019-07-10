
#共用的配置
class Base(object):
    xx = 123

#线上环境
class Pro(Base):
    DEBUG = False


#开发环境
class Dev(object):
    DEBUG = True