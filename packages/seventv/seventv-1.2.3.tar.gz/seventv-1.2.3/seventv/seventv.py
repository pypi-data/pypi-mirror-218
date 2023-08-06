from __future__ import annotations
import aiohttp

class Emote:
    def __init__(self, id, name, owner_username, host_url):
        self.id = id
        self.name = name
        self.owner_username = owner_username
        self.host_url = host_url

    def __repr__(self):
        return '' \
            f'Emote(id: {self.id}, ' \
            f'name: {self.name}, ' \
            f'owner_username: {self.owner_username}, ' \
            f'host_url: {self.host_url})'
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_username": self.owner_username,
            "host_url": self.host_url
        }

def create_emote_objects(response: dict) -> list[Emote]:
    emotes_data = response['data']['emotes']
    emote_items = emotes_data['items']

    emote_objects = []

    for emote in emote_items:
        emote_id = emote['id']
        emote_name = emote['name']
        owner = emote['owner']
        owner_username = owner['username']
        host = emote['host']
        host_url = host['url']
        emote_objects.append(Emote(emote_id, emote_name, owner_username, host_url))
    return emote_objects

class seventv:
    def __init__(self):
        self.endpoint = "https://7tv.io/v3/gql"
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def emote_search(self, 
                           searchterm: str = "", 
                           limit: int = 12, 
                           case_sensitive: bool = False, 
                           animated: bool = False,
                           exact_match: bool = False
                           ):
        url = self.endpoint
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "operationName": "SearchEmotes",
            "variables": {
                "query": searchterm,
                "limit": limit,
                "page": 1,
                "sort": {
                    "value": "popularity",
                    "order": "DESCENDING"
                },
                "filter": {
                    "category": "TOP",
                    "exact_match": exact_match,
                    "case_sensitive": case_sensitive,
                    "ignore_tags": False,
                    "zero_width": False,
                    "animated": animated,
                    "aspect_ratio": ""
                }
            },
            "query": "query SearchEmotes($query: String!, $page: Int, $sort: Sort, $limit: Int, $filter: EmoteSearchFilter) {\n  emotes(query: $query, page: $page, sort: $sort, limit: $limit, filter: $filter) {\n    count\n    items {\n      id\n      name\n      state\n      trending\n      owner {\n        id\n        username\n        display_name\n        style {\n          color\n          paint_id\n          __typename\n        }\n        __typename\n      }\n      flags\n      host {\n        url\n        files {\n          name\n          format\n          width\n          height\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
        }

        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                raise Exception("HTTP request failed")
            response_data = await response.json()
            emote_objects = create_emote_objects(response_data)
            return emote_objects

