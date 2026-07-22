from typing import Any, Generic, Optional, TypeVar


NVT = TypeVar('NVT', default=Any)

class Node(Generic[NVT]):
    
    __slots__ = ('value', 'parent', 'childs')
    
    value: NVT
    parent: Optional[Node]
    childs: dict[Any, Node]

    def __init__(self, value: NVT = None, parent: Optional[Node] = None) -> None:
        self.value = value
        self.parent = parent
        self.childs = dict()
    
    def __getitem__(self, _keys: Any) -> Optional[Node]:
        keys = self._to_tuple(_keys)
        cn = self
        for k in keys:
            cn = cn.childs.get(k, None)
            if cn is None:
                return
        return cn

    def __setitem__(self, _keys: Any, value: Any) -> None:
        keys = self._to_tuple(_keys)
        cn = self
        for k in keys:
            cn = cn.childs.setdefault(k, Node(parent=cn))
        cn.value = value

    @staticmethod
    def _to_tuple(keys: Any) -> tuple[Any, ...]:
        return keys if isinstance(keys, tuple) else (keys, ) # type: ignore
    
    @property
    def is_root(self) -> bool:
        return self.parent is None

    @property
    def is_leaf(self) -> bool:
        return not self.childs
    
    @property
    def dict(self) -> dict[str, Any]:
        return {'value': self.value, 'subnodes': {key: sn.dict for key, sn in self.childs.items()}}


__all__ = [
    'Node',
]