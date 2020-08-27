from dataclasses import dataclass
from typing import Tuple, Optional


@dataclass(eq=True, frozen=True)
class Material:
    name: str
    texture_file_path: Optional[str]
    metallic: float = 0.55
    roughness: float = 0.5
    alpha: float = 1.0
    scale: Tuple[float, float, float] = (1, 1, 1)
    rotation: Tuple[float, float, float] = (0, 0, 0)
    use_texture_for_displacement: bool = True
