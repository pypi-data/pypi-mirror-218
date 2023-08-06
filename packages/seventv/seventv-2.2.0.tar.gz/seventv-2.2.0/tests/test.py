import seventv
import asyncio

async def get():
    em=seventv.seventv()
    resp = await em.emote_search("balls", limit=1, query="url")
    print(resp[0].name)
    print(f'https:{resp[0].host_url}/2x.webp')
    await em.close()

asyncio.run(get())

""" respo = {'errors': [{'message': '70429 Rate Limit Reached', 'path': ['emotes'], 'extensions': {'code': 70429, 'fields': {}, 'message': 'Rate Limit Reached'}}], 'data': {'emotes': None}}
print(bool(respo.get('errors', {})))
print(respo.get('errors', {})[0].get('message', {})) """

""" from typing import Literal

def hmm(ok = Literal["wow", "bruh"]):
    dicty = {
        "wow": "1",
        "bruh": "not1"
    }
    dic = dicty.get(ok)
    test = {
        "value": dic 
    }
    print(test)

hmm("wow") """