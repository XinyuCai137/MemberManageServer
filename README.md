# 中国科学技术大学学生合唱团团员管理系统
中国科学技术大学生合唱团成立于2005年，经过13年的发展，现已成为科大诸多社团中最为优秀的社团之一，连续5年获得“五星社团”。然而社团的团务工作十分繁杂，合唱团一直致力于将团务工作标准化，有利于减轻团务同学负担、团务工作的传承。其中招新与团员管理就是非常重要的一部分。本系统致力于构建一个web应用来实现合唱团运营团员管理的工作。

---
## 需求分析
### 1. 招新 

合唱团招新主要分为两部分，一是每学年9月面对新生的集中招新面试，二是全年任何时间的单独的招新面试。

但是面试报名需要填写线下纸质表单，面试成绩和是否通过面试要手动统计、审批，十分低效。

### 2. 团员管理

学生合唱团虽然只有团员不足百人，但是却又较为复杂的关系：

- 团员的姓名、性别、学号、学院等基本属性
- 根据业务结构分为指挥（C）、钢琴伴奏（P）、和女高音（S）、女低音（A）、男高音（T）、男低音（B）四个声部，每个声部内又分1、2（如S1和S2）每个声部有1-2个声部长，钢琴伴奏和同时又属于4个声部
- 根据团务结构可以分为六个部门：财物部、技术部、媒体部、事务部、外联部、宣传部

一直以来团员管理的都是手动在Excel中完成，较为低效，甚至是缺失的 

---
## 设计目标

### 终极目标：

​	设计一个完善的网站，所有合唱团相关的内容（宣传、活动、录音、通知等）都可以在网站上发布

​	通过用户（团员注册成为用户）管理的方式管理团员

### 本系统实现目标：

#### 1. 面试

​	非团员在网站上报名面试

​	管理员在面试中通过本系统评分

​	管理员审核可以通过面试的面试者

​	面试者通过面试后可以在本站注册成为团员

​		

```flow
st=>start: 报名面试
ms=>operation: 参加面试，面试官评分
select=>operation: 确定是否通过面试
op=>operation: 面试失败
cond=>condition: 通过
register=>operation: 注册

e=>end: 成为团员
st->ms->select->cond
cond(yes)->register->e
cond(no)->op
```

#### 2. 团员管理

网站中分为普通团员和管理员两种权限

团员视图：

- 查看&修改个人信息

- 查询团员信息

管理员视图：

- 团员视图

- 修改团员信息（只能修改声部与部门不能修改个人信息）

- 面试评分

- 面试审核

---

## 关系数据库设计

### 概念结构设计

#### 面试者属性（Interviewer）

面试者学号->（姓名、性别、院系、手机、是否通过）

#### 面试属性（Interview）

允许多次面试

面试者学号->（面试时间、成绩）

#### 团员属性（Member）

学号->（姓名、性别、院系、声部、部门、邮箱、手机、权限）

#### 其他属性

部门->部长（Department）

声部->声部长（Voice Part）

学院->校区（School）

#### E-R图

![E-R](C:\Users\27318\Documents\Vegelofe\USTChorusServer\www\static\sql\E-R.png)

### 逻辑结构设计

#### 建立数据库(www/static/sql/create_db.sql)

```mysql
DROP DATABASE IF EXISTS chorus;

CREATE DATABASE chorus;

USE chorus;

GRANT SELECT, INSERT, UPDATE, DELETE ON awesome.* TO 'www-data'@'localhost' identified BY 'www-data';

CREATE TABLE interviewers (
    `stu_id` VARCHAR(10) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `name` VARCHAR(10) NOT NULL,
    `sex` VARCHAR(10) NOT NULL,
    `school` VARCHAR(30) NOT NULL,
    `phone` VARCHAR(20) NOT NULL,
    `passed` BOOL NOT NULL,
    `image` VARCHAR(500),
    `created_at` REAL NOT NULL,
    UNIQUE KEY `idx_email` (`email`),
    KEY `idx_created_at` (`created_at`),
    PRIMARY KEY (`stu_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE interviews (
	`stu_id` VARCHAR(50) NOT NULL, 
	`grade_1` INT,
	`grade_2` INT,
	`grade_3` INT,
	`grade_4` INT,
	`grade_5` INT,
	`extra` VARCHAR(500),
    `created_at` REAL NOT NULL,
    KEY `idx_created_at` (`created_at`),
	PRIMARY KEY (`stu_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE members (
    `stu_id` VARCHAR(10) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    `passwd` VARCHAR(50) NOT NULL,
    `name` VARCHAR(10) NOT NULL,
    `sex` VARCHAR(10) NOT NULL, 
    `school` VARCHAR(30) NOT NULL,
    `voice_part` VARCHAR(2) NOT NULL,
    `department` VARCHAR(10) NOT NULL,
    `phone` VARCHAR(20) NOT NULL,
    `admin` BOOL NOT NULL,
    `image` VARCHAR(500) NOT NULL,
    `created_at` REAL NOT NULL,
    UNIQUE KEY `idx_email` (`email`),
    KEY `idx_created_at` (`created_at`),
    PRIMARY KEY (`stu_id`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE schools (
	`school` VARCHAR(30) NOT NULL,
	`campus` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`school`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE voice_parts (
    `voice_part` VARCHAR(2) NOT NULL,
	`vp_lead1` VARCHAR(10) NOT NULL,
	`vp_lead2` VARCHAR(10),
    PRIMARY KEY (`voice_part`)
) ENGINE=innodb DEFAULT CHARSET=utf8;

CREATE TABLE departments (
    `department` VARCHAR(10) NOT NULL,
    `dep_lead` VARCHAR(10) NOT NULL,
    PRIMARY KEY (`department`)
) ENGINE=innodb DEFAULT CHARSET=utf8;
```

#### 数据库初始化(www/static/sql/init.sql)

```mysql
INSERT INTO chorus.departments (department, dep_lead) VALUES ('外联部','蔡心宇'), ('财物部','吴宁谦'), ('宣传部','叶百家'), ('媒体部','白子逸'), ('技术部','白子逸'), ('事务部','林雪森')

INSERT INTO chorus.schools (school, campus) VALUES ('少年班学院','东校区'), ('数学科学学院','东校区'), ('物理学院','东校区'), ('管理学院','东校区'), ('化学与材料科学学院','东校区'), ('地球和空间科学学院','东校区'), ('人文与社会科学学院','东校区'), ('工程科学学院','西校区'), ('信息科学技术学院','西校区'), ('计算机科学与技术学院','西校区'), ('网络空间安全学院','西校区'), ('软件学院','西校区')

INSERT INTO chorus.voice_parts (voice_part, vp_lead1, vp_lead2) VALUES ('S', '李居龄', '曾嘉忻'), ('A', '时瑞', '韩江萍'), ('T', '白子逸', '陈淦斌'), ('B', '齐燕处', '叶百家')

INSERT INTO chorus.voice_parts (voice_part, vp_lead1) VALUES ('C', '钱泽华'), ('P', '钱泽华')
```

## 实现
本应用后端使用Python作为服务器后端语言、Mysql作为关系数据库管理系统搭建

前端使用Html、Javascript，其中用到了Js框架[Vue](https://cn.vuejs.org/v2/guide/)

主要参考了[廖雪峰的python教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)、[w3school](http://www.w3school.com.cn/)、[老马的Vue教程](https://www.aicoder.com/vue/preview/all.html#1)

### 搭建开发环境

首先，确认系统安装的Python版本是3.6.x：

```
$ python3 --version
Python 3.6.1
```

然后，用`pip`安装开发Web App需要的第三方库：

异步框架aiohttp：

```
$pip3 install aiohttp
```

前端模板引擎jinja2：

```
$ pip3 install jinja2
```

MySQL数据库，从老师课程主页下载，设置root口令。

MySQL的Python异步驱动程序aiomysql：

```
$ pip3 install aiomysql
```

---



### 项目结构

选择一个工作目录，然后，我们建立如下的目录结构：

```
USTChorusServer/  <-- 根目录
|
+- www/                  <-- Web目录，存放.py文件
|  |
|  +- static/            <-- 存放静态文件
|  |  |
|  |  +- css/			 <-- 存放css库
|  |  |
|  |  +- fonts/			 <-- 存放字体文件
|  |  |
|  |  +- img/			 <-- 存放图片文件
|  |  |
|  |  +- js/			 <-- 存放js库
|  |  |
|  |  +- sql/  			 <-- 存放建立数据库及测试用的sql文件
|  |
|  +- templates/         <-- 存放模板文件（html）
```

---



### 封装DML(www/orm.py)

访问数据库需要创建数据库连接、游标对象，然后执行SQL语句，最后处理异常，清理资源。这些访问数据库的代码如果分散到各个函数中，势必无法维护，也不利于代码复用。

为了使用的方便性，首先把常用的SELECT、INSERT、UPDATE和DELETE操作封装起来。

#### Select

要执行SELECT语句，我们用`select`函数执行，需要传入SQL语句和SQL参数：

```python
@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs
```

SQL语句的占位符是`?`，而MySQL的占位符是`%s`，`select()`函数在内部自动替换。注意要始终坚持使用带参数的SQL，而不是自己拼接SQL字符串，这样可以防止SQL注入攻击。

注意到`yield from`将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果。

如果传入`size`参数，就通过`fetchmany()`获取最多指定数量的记录，否则，通过`fetchall()`获取所有记录。

#### Insert, Update, Delete

要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的`execute()`函数，因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数：

```python
@asyncio.coroutine
def execute(sql, args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected
```

`execute()`函数和`select()`函数所不同的是，cursor对象不返回结果集，而是通过`rowcount`返回结果数。

---



### 编写ORM

[ORM](https://baike.baidu.com/item/ORM)对象关系映射(Object Relational Mapping），是一种程序技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。从效果上说，它其实是创建了一个可在编程语言里使用的--“虚拟对象数据库”。

#### 定义用于映射数据库内数据类型的Field(www/orm.py)

例如`StringField`对应`varchar`

```python
class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)

class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):

    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)
```

#### 定义与数据库中各个表对应的Models((www/models.py))

例如`class Interviewers`对应`TABLE interviewers`

```python
class Interviewers(Model):
    __table__ = 'interviewers'

    stu_id = StringField(primary_key=True, ddl='varchar(10)')
    email = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(10)')
    sex = StringField(ddl='varchar(10)')
    school = StringField(ddl='varchar(30)')
    phone = StringField(ddl='varchar(20)')
    passed = BooleanField()
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Interviews(Model):
    __table__ = 'interviews'
    
    stu_id = StringField(primary_key=True, ddl='varchar(10)')
    created_at = FloatField(default=time.time)
    grade_1 = IntegerField()
    grade_2 = IntegerField()
    grade_3 = IntegerField()
    grade_4 = IntegerField()
    grade_5 = IntegerField()
    extra = StringField(ddl='varchar(500)')

class Members(Model):
    __table__ = 'members'

    stu_id = StringField(primary_key=True, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    sex = StringField(ddl='varchar(10)')
    school = StringField(ddl='varchar(30)')
    voice_part = StringField(ddl='varchar(2)')
    department = StringField(ddl='varchar(10)')
    phone = StringField(ddl='varchar(20)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)

class Schools(Model):
    __table__ = 'schools'

    school = StringField(primary_key=True, ddl='varchar(30)')
    campus = StringField(ddl='varchar(10)')

class Voice_parts(Model):
    __table__ = 'voice_parts'

    voice_part = StringField(primary_key=True, ddl='varchar(2)')
    vp_lead1 = StringField(ddl='varchar(10)')
    vp_lead2 = StringField(ddl='varchar(10)')

class Departments(Model):
    __table__ = 'departments'

    department = StringField(primary_key=True, ddl='varchar(10)')
    dep_lead = StringField(ddl='varchar(10)')
```

这些对象都继承自`Model`，其定义在`orm.py`中

```python
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                logging.info('  found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        raise StandardError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    @asyncio.coroutine
    def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = yield from select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    @asyncio.coroutine
    def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = yield from select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    @asyncio.coroutine
    def find(cls, pk):
        ' find object by primary key. '
        rs = yield from select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @asyncio.coroutine
    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = yield from execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    @asyncio.coroutine
    def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = yield from execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    @asyncio.coroutine
    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = yield from execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
```

`Model`对象中定义了用于在本表中定义了`findAll` `findNumber` `find`用于查询， `save`用于插入 ，`update`用于更新， `remove`用于删除

**在本系统中，并没用直接用SQL语言进行连接查询或者子查询；而是在主语言Python中使用上述函数实现相同功能，在后文中可以看到清晰的例子**

---

### 编写server骨架

使用`aiohttp`构建一个web app

使用`asyncio`异步IO模块建立一个事件循环，并把web app放进去，异步处理http请求的后端骨架就搭好了

（www/app.py）

```python
import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

@asyncio.coroutine
def init(loop):
    yield from orm.create_pool(loop=loop, **configs.db)
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
```



### 编写web框架

因为`aiohttp`相对比较底层，所以还需要将其封装一下，目的是为了在后期实现各种后端处理函数时可以减少所编写的代码

`aiohttp`处理一个URL需要：

1. 从`request`中提取参数

2. 使用URL处理函数处理

3. 构造`web.Response`返回

首先说明第二部分的实现

#### 定义@get和@post装饰器

Http请求分`get`和`post`两种方法，用户发来的http请求中，包含请求的URL和方法，所以定义两种方法的装饰器，之后再编写请求处理函数时用`@get`和`@post`装饰即可

```python
def get(path):
    '''
    Define decorator @get('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    Define decorator @post('/path')
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator
```

例如返回主页的URL处理函数：

```python
@get('/')
def index(request):
    return {
        '__template__': 'index.html'
    }
```

对于不同URL和方法的请求，只需按照上面的形式添加即可



#### 定义RequestHandler

接下来第一部分——如何获取参数。

用`RequestHandler()`来封装一个URL处理函数。

`RequestHandler`是一个类，由于定义了`__call__()`方法，因此可以将其实例视为函数。

`RequestHandler`目的就是从URL函数中分析其需要接收的参数，从`request`中获取必要的参数，调用URL函数，然后把结果转换为`web.Response`对象，这样，就完全符合`aiohttp`框架的要求：

```python
class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn
        ...

    @asyncio.coroutine
    def __call__(self, request):
        kw = ... 获取参数
        r = yield from self._func(**kw)
        return r
```

在`__call__`中首先先从request中获取参数，然后调用`self._func`，即上文中讲的使用`@get`和`@post`装饰的URL处理函数，这里需要注意的是，每个由`@get`和`@post`装饰的URL处理函数对应一个`RequestHandler`实例。



#### 使用middlewares

在`app.py`中有

```python
app = web.Application(loop=loop, middlewares=[
    logger_factory, auth_factory, response_factory
])
```

`logger_factory`、`response_factory`和`auth_factory`，定义如下：

```python
@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (yield from handler(request))
    return logger

@asyncio.coroutine
def auth_factory(app, handler):
    @asyncio.coroutine
    def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = yield from cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        if request.path.startswith('/user/') and (request.__user__ is None):
            return web.HTTPFound('/signin')        
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        return (yield from handler(request))
    return auth

@asyncio.coroutine
def response_factory(app, handler):
    @asyncio.coroutine
    def response(request):
        logging.info('Response handler...')
        r = yield from handler(request)
        
        ...
        
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

```

`middlewares`是`aiohttp`中提供的拦截器，一个URL在被某个函数处理前，可以经过一系列的`middleware`的处理。

一个`middleware`可以改变URL的输入、输出，甚至可以决定不继续处理而直接返回。`middleware`的用处就在于把通用的功能从每个URL处理函数中拿出来，集中放到一个地方。

`logger_factory`是用来记录日志，`auth_factory`会使用`cookie`来认证用户权限，这部分将在后面提到`response_factory`是用来处理后端发给浏览器的http响应。



**上述处理过程比较复杂，难以理解，下边的流程图可以更形象地描绘函数调用关系**

```flow
st=>start: 收到http request
ms=>operation: middleware拦截
log=>operation: logger_factory记录日志 
auth=>operation: auth_factory认证用户权限
res1=>operation: response_factory调用handler
res2=>operation: 产生response返回response_factory
res2=>operation: 最后处理response
call=>operation: RequestHandler.__call__
call1=>operation: 提取request参数
@=>operation: @get/@post函数处理具体事务
e=>end: 返回response
st->ms->log->auth->res1->call->call1->@->res2->e
```

至此后端处理http request并返回response框架已经完成

---



### 编写MVC



### 报名面试



### 面试评分



### 面试审核



### 用户注册与登录



### 个人信息



### 查询页面




