from typing import List, Optional

from pydantic import BaseModel

from .commands import CommandContribution
from .menus import MenusContribution
from .readers import ReaderContribution
from .sample_data import SampleDataContribution, SampleDataGenerator, SampleDataURI
from .submenu import SubmenuContribution
from .themes import ThemeContribution
from .widgets import WidgetContribution
from .writers import WriterContribution

__all__ = [
    "ContributionPoints",
    "CommandContribution",
    "MenusContribution",
    "ReaderContribution",
    "SampleDataContribution",
    "SubmenuContribution",
    "ThemeContribution",
    "WidgetContribution",
    "WriterContribution",
    "SampleDataGenerator",
    "SampleDataURI",
]


class ContributionPoints(BaseModel):
    commands: Optional[List[CommandContribution]]
    themes: Optional[List[ThemeContribution]]
    readers: Optional[List[ReaderContribution]]
    writers: Optional[List[WriterContribution]]
    sample_data: Optional[List[SampleDataContribution]]
    widgets: Optional[List[WidgetContribution]]

    menus: Optional[MenusContribution]
    submenus: Optional[List[SubmenuContribution]]

    # configuration: Optional[JsonSchemaObject]
    # keybindings: Optional[List[KeyBindingContribution]]
