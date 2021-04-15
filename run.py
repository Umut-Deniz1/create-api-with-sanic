import asyncio
import aiomysql
import json as myJson
from sanic import Sanic
from sanic.response import json,text
from time import time
import requests
import nest_asyncio

nest_asyncio.apply()

loop = asyncio.get_event_loop()


@asyncio.coroutine
def test_example(ID):
    _query = "SELECT  *  from node-app.product where id={}".format(ID)

    conn = yield from aiomysql.connect(host='localhost', port=3306, user='root', password='12345', db='node-app')

    cursor = yield from conn.cursor(aiomysql.DictCursor)

    yield from cursor.execute(_query)
    global data

    r = yield from cursor.fetchone()
    data = myJson.dumps(r)
    return json(data)



app = Sanic(__name__)

@app.route('/db')
async def tag_handler(request):
    ID = request.args.get('id')
    result = loop.run_until_complete(test_example(ID=ID))
    return (result)




if __name__ == "__main__":
    app.run()
