# seventv
an asynchronous Python API-wrapper for [7tv.app](https://7tv.app)

This API-wrapper makes use of the 7tv API (v3) to make it possible to get emotes, details about them, and soon some more things the API supports.

To get emotes by search query, the wrapper uses the GraphQL endpoint ```https://7tv.io/v3/gql``` because it seems to currently be the only working one for searching emotes. 

# Installation
## How to install:
```
pip install seventv
```
### requires:
```
aiohttp
```

# Usage
To search for an emote and make use of the search results, do the following (asynchronously):
- create a class instance of sevenTV
- await the ```.emote_search``` method with your search query string and optional filters
- don't forget to close the session at some later point, using ```.close()```.

Example usage:
```
import asyncio
import seventv

async def myFunctionSearchEmote():
    mySeventvSession = seventv() # initialize the session
    
    emotes = await mySeventvSession.emote_search("pepe", case_sensitive=True)
    # searches for "pepe", using the optional filter "case_sensitive"
    
    print(emotes[2]) # get the third emote from the search results
    await mySeventvSession.close() # later close the session

asyncio.run(getemote())
```

Sample output: third Emote object in the search results:
```Emote(id: 60a304efac2bcb20ef20fa89, name: pepeMeltdown, owner_username: supernoahtv, host_url: //cdn.7tv.app/emote/60a304efac2bcb20ef20fa89)```

The output from a search is an array with the Emote objects inside.
Each emote contains the following properties:
- id
- name
- owner_username
- host_url

_Sidenote: Keep in mind that to get the emote using the url, the file extension must be appended to the host_url. Emotes are stored on 7tv in different sizes, usually ranging from 1x.webp to 4x.webp. Not every emote might have every size though, so look it up or go with x2 or x3 which the majority of emotes have._

### Currently available search filters (optional):

| filter                         | meaning | default value |     
| ---------------------------------------------- | -------- | --------------- | 
| limit (int) | how many emotes are contained in the response      | 12             |     
| case_sensitive (bool)                         | whether or not upper-/lowercase letters are treated differently or will not be distinguished      | False             |     
| animated (bool)                                     |only return animated emotes in search results          | False                 |     
| ---more to be added soon---                                  |          |                 |     |                                               |          |                 |     


soon to be added functionality: 
- more search filters
- getting an emote by it's id