import ORM
from ORM import Model, StringField, IntegerField
import asyncio


class User(Model):
    __table__ = 'user'

    id = IntegerField(primary_key=True)
    name = StringField()


async def connectDB(loop):
    username = 'root'
    password = 'password'
    dbname = 'test'
    await ORM.create_pool(loop, user=username, password=password, db=dbname)

async def destoryDB():
    await ORM.destory_pool()


async def testsave(loop):
    await connectDB(loop)
    user = User(id="125", name='Yaoda',sex='male')
    await user.save()
    print(user)
    await destoryDB()

async def testupdate(loop):
    await connectDB(loop)
    user = await User.find(5)
    if user:
        user.name = 'Yaoda'
        await user.update()
        print('user update:%s' % user)
    await destoryDB()

async def testfind(loop):
    await connectDB(loop)
    r = await User.find(5)
    print(r)
    await destoryDB()

async def testfindall(loop):
    await connectDB(loop)
    r = await User.findAll()
    print(r)
    await destoryDB()

async def testremove(loop):
    await connectDB(loop)
    user = await User.find(1)
    await user.remove()
    await destoryDB()

loop = asyncio.get_event_loop()
loop.run_until_complete(testsave(loop))
loop.run_until_complete(testfindall(loop))


