from dataclasses import dataclass
from typing import Tuple


@dataclass(eq=True, frozen=True)
class Material:
    name: str
    texture_file_path: str
    metallic: float = 0.55
    roughness: float = 0.5
    scale: Tuple[float, float, float] = (1, 1, 1)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    displacement: bool = True
