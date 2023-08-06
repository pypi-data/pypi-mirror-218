import seventv
import asyncio

async def get():
    em=seventv.seventv()
    query = "wow huh"
    resp = await em.emote_search("pepe")
    print(resp)
    #print(f'https:{resp[0].host_url}/2x.webp')
    await em.close()

asyncio.run(get())