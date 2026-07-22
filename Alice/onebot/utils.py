from typing import Any, Optional, TYPE_CHECKING

from Alice.core.utils import get_subclass
from Alice.lib.tree import Node
from Alice.onebot.event import Event

if TYPE_CHECKING:
    from Alice.core.bot.bot import AliceBot


#region 解析Onebot事件
_POST_TYPES = {'message': 'message_type', 'message_sent': 'message_type', 'meta_event': 'meta_event_type', 'notice': 'notice_type', 'request': 'request_type'}

def _generate_event_tree() -> Node:
    event_subclass = get_subclass(Event)
    TREE = Node(Event)
    for event in event_subclass:
        pt = event.model_fields.get('post_type', None)
        rt = None
        st = event.model_fields.get('sub_type', None)
        for spt in _POST_TYPES.values():
            if rt := event.model_fields.get(spt, None):
                break
        pt_v = pt.default if pt and not pt.is_required() else None
        rt_v = rt.default if rt and not rt.is_required() else None
        st_v = st.default if st and not st.is_required() else None
        if not any((pt_v, rt_v, st_v)):
            continue
        if rt_v is None:
            TREE[pt_v] = event
            continue
        if st_v is None:
            TREE[pt_v, rt_v] = event
            continue
        TREE[pt_v, rt_v, st_v] = event
    return TREE

_EVENT_TREE = _generate_event_tree()
del _generate_event_tree    

def parse_raw_onebot_event(bot: AliceBot, data: dict[str, Any]) -> Optional[Event]:
    pt = data.get('post_type', None)
    if pt is None:
        return None
    node = _EVENT_TREE[pt]
    if node is None:
        return None
    if rt := data.get(_POST_TYPES[pt], None):
        node = node[rt] or node
        if st:= data.get('sub_type', None):
            node = node[st] or node
    event = node.value(bot=bot, **data)
    return event
#endregion


__all__ = [
    'parse_raw_onebot_event',
]