from seventv.seventv import Emote, create_emote_objects, seventv

__all__ = [
    'Emote',
    'create_emote_objects',
    'seventv',
]

default_client = seventv()
emote_search = default_client.emote_search
__all__.append('emote_search')