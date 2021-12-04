import os
import warnings
from importlib import metadata
from typing import Iterable, Tuple

PLUGIN = os.getenv("NAPARI_PLUGIN")
if not PLUGIN:
    raise ValueError(
        "This test requires that you specify a plugin with the NAPARI_PLUGIN env var"
    )


def plugin_entrypoints(package) -> Iterable[Tuple[str, str]]:
    for ep in metadata.distribution(package).entry_points:
        if ep.group != "napari.plugin":
            continue
        yield (ep.name, ep.value)


def test_plugin_detected():
    from napari.plugins import plugin_manager

    with warnings.catch_warnings():
        # don't let warnings on import fail the test
        warnings.simplefilter("ignore")
        for err in plugin_manager.discover()[1]:
            print(err.format())

    eps = list(plugin_entrypoints(PLUGIN))
    assert eps

    for name, ep in eps:
        assert name in plugin_manager.plugins
