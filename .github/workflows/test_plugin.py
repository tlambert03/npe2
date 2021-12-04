from __future__ import annotations

import os
import warnings
from importlib import metadata
from typing import TYPE_CHECKING, Iterable, Tuple

import pytest

if TYPE_CHECKING:
    from napari.plugins import NapariPluginManager as PM


PLUGIN = os.getenv("NAPARI_PLUGIN")
if not PLUGIN:
    raise ValueError(
        "This test requires that you specify a plugin with the NAPARI_PLUGIN env var"
    )


@pytest.fixture(scope="session")
def plugin_manager():
    from napari.plugins import plugin_manager

    with warnings.catch_warnings():
        # don't let warnings on import fail the test
        warnings.simplefilter("ignore")
        for err in plugin_manager.discover()[1]:
            print(err.format())
        plugin_manager.discover_widgets()

    return plugin_manager


def plugin_entrypoints(package) -> Iterable[Tuple[str, str]]:
    for ep in metadata.distribution(package).entry_points:
        if ep.group == "napari.plugin":
            yield (ep.name, ep.value)


def test_declares_entry_point():
    assert list(plugin_entrypoints(PLUGIN))


@pytest.mark.skip
def test_not_abusing_entry_point(plugin_manager: PM):
    """Test that a plugin module actually provides a hookspec.

    Otherwise, they're likely abusing the entry point for import side-effects
    (should be solved with npe2)
    """
    for module, callers in plugin_manager._plugin2hookcallers.items():
        name = module.__name__
        if name != "napari_console":
            assert callers, f"Plugin module {name!r} imported but has no hookspecs!"


def test_plugin_detected(plugin_manager: PM):
    """Test the plugin module was actually registered by the plugin manager"""
    mods = [mod.__name__ for mod in plugin_manager._plugin2hookcallers]
    for _, mod in plugin_entrypoints(PLUGIN):
        assert mod in mods


def test_dock_widgets(qtbot, make_napari_viewer, plugin_manager: PM, monkeypatch):
    """Test that dock widgets can be created"""

    # weird, but safe way to get the plugin name
    # using the module rather than the name
    hook = plugin_manager.hook.napari_experimental_provide_dock_widget
    for _, mod in plugin_entrypoints(PLUGIN):
        for impl in hook.get_hookimpls():
            if impl.plugin.__name__ != mod:
                continue
            wdgs = impl.function()
            if not wdgs:
                continue
            wdgs = wdgs if isinstance(wdgs, list) else [wdgs]
            for item in wdgs:
                wdg = item[0] if isinstance(item, tuple) else item
                assert callable(wdg)

                # this would be better, but could yield a lot of false errors
                # wdg = _instantiate_dock_widget(wdg, make_napari_viewer)
                # qtbot.addWidget(wdg)


def test_single_backend_installed():
    try:
        pass
    except ImportError:
        assert __import__("PyQt5"), "No backend installed?"
    else:
        try:
            pass
        except ImportError:
            pass
        else:
            raise AssertionError("Multiple backends installed")


def _instantiate_dock_widget(wdg_cls, make_viewer):
    # if the signature is looking a for a napari viewer, pass it.
    import inspect

    from napari.viewer import Viewer

    kwargs = {}
    try:
        sig = inspect.signature(wdg_cls.__init__)
    except ValueError:
        pass
    else:
        for param in sig.parameters.values():
            if param.name == "napari_viewer":
                kwargs["napari_viewer"] = make_viewer()
                break
            if param.annotation in ("napari.viewer.Viewer", Viewer):
                kwargs[param.name] = make_viewer()
                break

    # instantiate the widget
    wdg = wdg_cls(**kwargs)
    return wdg.native if hasattr(wdg, "native") else wdg
