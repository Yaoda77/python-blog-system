
import asyncio, logging

import aiomysql

async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' %len(rs))
        return rs

#define function to execute insert, update and delete for SQL
async def execute(sql, args):
    log(sql)
    async with __pool.get() as conn:
        try:
            cur = =await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
        except BaseException as e:
            raise
        return affected

from orm import Model, StringField, IntegerField

class User(Model):
    __table__ = 'users'
    #the structure of table:
    id = IntegerField(primary_key=True)
    name = StringField()

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(selfself, key, value):
        self[key] = value

    def getValue(self, key):
        return  getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('using default value for %s: %s' %(key,str(value)))
                setattr(self, key, value)
            return value

class Field(object):

    def __init__(selfself, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' %(self.__class__.__name__,self.column_type, self.name)

class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None):
        super().__init__(name, ddl, primary_key, default)

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        #except Model class itself:
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        #get the name of table:
        tableName = attrs.get('__table__', None) or name