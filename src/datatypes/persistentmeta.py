from dataclasses import dataclass, field
from typing import Any


# todo: map support for persistent meta?
@dataclass
class PersistentMeta:
    startup_instances: int
    args: dict[str, Any] = field(default_factory=dict)