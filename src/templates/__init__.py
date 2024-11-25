from pathlib import Path

from promplate_recipes.context import ComponentsLayer, layers

layers.append(compoennts := ComponentsLayer(Path(__file__).parent))

__getattr__ = compoennts.__getitem__
