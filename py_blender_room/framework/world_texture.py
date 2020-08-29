from dataclasses import dataclass
from typing import Tuple


@dataclass
class WorldTexture:
    path_to_texture_file: str
    rotation: Tuple[float, float, float] = (0, 0, 0)
    scale: Tuple[float, float, float] = (1, 1, 1)
    location: Tuple[float, float, float] = (0, 0, 0)
