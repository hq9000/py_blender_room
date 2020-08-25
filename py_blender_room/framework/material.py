from dataclasses import dataclass
from typing import Tuple


@dataclass
class Material:
    name: str
    texture_file_path: str
    metallic: float = 0.55
    scale: Tuple[float, float, float] = (1, 1, 1)
    rotation: Tuple[float, float, float] = (0, 0, 0)

