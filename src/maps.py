"""
Module with some maps of the levels.
"""
import pytmx
from pygame.surface import Surface

from src.scrolling import Scroll
from src.settings import ROOT_DIR


class TiledMap:

    _total_map_width: int
    _total_map_height: int
    _tmx_map: pytmx.TiledMap  # parsed tmx data

    def __init__(self, map_file_name: str, assets_maps_folder: str = "assets/maps") -> None:
        tm = pytmx.load_pygame(ROOT_DIR.joinpath(assets_maps_folder, map_file_name), pixelalpha=True)

        self._total_map_width = tm.width * tm.tilewidth
        self._total_map_height = tm.height * tm.tileheight
        self._tmx_map = tm

    @property
    def total_map_width(self) -> int:
        return self._total_map_width

    @property
    def total_map_height(self) -> int:
        return self._total_map_height

    @property
    def tmx_map(self) -> pytmx.TiledMap:
        return self._tmx_map

    def render_on(self, raw_display: Surface, scroll: Scroll) -> None:
        for visible_layer in self._tmx_map.visible_layers:
            # only visible layers
            if isinstance(visible_layer, pytmx.TiledTileLayer):
                for x, y, gid in visible_layer:
                    tile: Surface = self._tmx_map.get_tile_image_by_gid(gid)

                    if tile is not None:
                        raw_display.blit(
                            tile,
                            (
                                x * self._tmx_map.tilewidth - scroll.offset_x,
                                y * self._tmx_map.tileheight - scroll.offset_y,
                            ),
                        )
