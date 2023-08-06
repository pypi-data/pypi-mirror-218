from seventv import seventv
import asyncio

async def get():
    em=seventv()
    resp = await em.emote_search(animated=True, case_sensitive=True)
    print(resp)
    await em.close()

asyncio.run(get())