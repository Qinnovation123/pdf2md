from pathlib import Path

from promplate_recipes.context import ComponentsLayer, layers

layers.append(components := ComponentsLayer(Path(__file__).parent))

__getattr__ = components.__getitem__
