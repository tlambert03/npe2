import configparser
import os
from importlib import metadata
from typing import Iterable, Tuple

PLUGIN = os.getenv("PLUGIN")
if not PLUGIN:
    raise ValueError(
        "This test requires that you specify a plugin with the PLUGIN env var"
    )


def plugin_entrypoints(package) -> Iterable[Tuple[str, str]]:
    p = configparser.ConfigParser()
    eps = metadata.distribution(package).read_text("entry_points.txt")
    if not eps:
        return
    p.read_string(eps)
    if "napari.plugin" not in p:
        return
    yield from p["napari.plugin"].items()


def test_plugin_detected():
    from napari.plugins import plugin_manager

    eps = list(plugin_entrypoints(PLUGIN))
    assert eps

    plugin_manager.discover()
    for name, ep in eps:
        assert name in plugin_manager.plugins
