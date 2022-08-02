import re
from abc import ABC, abstractmethod
from typing import Optional, Tuple

import napari
from napari._qt.containers import QtListView
from napari.qt import get_app
from napari.utils.events import SelectableEventedList
from qtpy.QtCore import (
    QAbstractItemModel,
    QEvent,
    QModelIndex,
    QObject,
    QRect,
    QSize,
    Qt,
)
from qtpy.QtGui import QFontMetrics, QPainter
from qtpy.QtWidgets import (
    QAbstractItemDelegate,
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QStyle,
    QStyleOptionViewItem,
    QTextEdit,
    QWidget,
)

from npe2.manifest.contributions import ConfigurationProperty

splitter = re.compile(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)")


def _split_camel(identifier: str) -> str:
    return " ".join([m.group(0).capitalize() for m in splitter.finditer(identifier)])


get_app()
true = True
false = False
null = None

properties = {
    "git.enabled": {
        "type": "boolean",
        "scope": "resource",
        "description": "%config.enabled%",
        "default": true,
    },
    "git.path": {
        "type": ["string", "null", "array"],
        "markdownDescription": "%config.path%",
        "default": null,
        "scope": "machine",
    },
    "git.autoRepositoryDetection": {
        "type": ["boolean", "string"],
        "enum": [true, false, "subFolders", "openEditors"],
        "enumDescriptions": [
            "%config.autoRepositoryDetection.true%",
            "%config.autoRepositoryDetection.false%",
            "%config.autoRepositoryDetection.subFolders%",
            "%config.autoRepositoryDetection.openEditors%",
        ],
        "description": "%config.autoRepositoryDetection%",
        "default": true,
    },
    "git.autorefresh": {
        "type": "boolean",
        "description": "%config.autorefresh%",
        "default": true,
    },
    "git.autofetch": {
        "type": ["boolean", "string"],
        "enum": [true, false, "all"],
        "scope": "resource",
        "markdownDescription": "%config.autofetch%",
        "default": false,
        "tags": ["usesOnlineServices"],
    },
    "git.autofetchPeriod": {
        "type": "number",
        "scope": "resource",
        "markdownDescription": "%config.autofetchPeriod%",
        "default": 180,
    },
    "git.branchPrefix": {
        "type": "string",
        "description": "%config.branchPrefix%",
        "default": "",
        "scope": "resource",
    },
    "git.branchProtection": {
        "type": "array",
        "markdownDescription": "%config.branchProtection%",
        "items": {"type": "string"},
        "default": [],
        "scope": "resource",
    },
    "git.branchProtectionPrompt": {
        "type": "string",
        "description": "%config.branchProtectionPrompt%",
        "enum": ["alwaysCommit", "alwaysCommitToNewBranch", "alwaysPrompt"],
        "enumDescriptions": [
            "%config.branchProtectionPrompt.alwaysCommit%",
            "%config.branchProtectionPrompt.alwaysCommitToNewBranch%",
            "%config.branchProtectionPrompt.alwaysPrompt%",
        ],
        "default": "alwaysPrompt",
        "scope": "resource",
    },
    "git.branchValidationRegex": {
        "type": "string",
        "description": "%config.branchValidationRegex%",
        "default": "",
    },
    "git.branchWhitespaceChar": {
        "type": "string",
        "description": "%config.branchWhitespaceChar%",
        "default": "-",
    },
    "git.branchRandomName.enable": {
        "type": "boolean",
        "description": "%config.branchRandomNameEnable%",
        "default": false,
        "scope": "resource",
    },
    "git.branchRandomName.dictionary": {
        "type": "array",
        "markdownDescription": "%config.branchRandomNameDictionary%",
        "items": {
            "type": "string",
            "enum": ["adjectives", "animals", "colors", "numbers"],
            "enumDescriptions": [
                "%config.branchRandomNameDictionary.adjectives%",
                "%config.branchRandomNameDictionary.animals%",
                "%config.branchRandomNameDictionary.colors%",
                "%config.branchRandomNameDictionary.numbers%",
            ],
        },
        "minItems": 1,
        "maxItems": 5,
        "default": ["adjectives", "animals"],
        "scope": "resource",
    },
    "git.confirmSync": {
        "type": "boolean",
        "description": "%config.confirmSync%",
        "default": true,
    },
    "git.countBadge": {
        "type": "string",
        "enum": ["all", "tracked", "off"],
        "enumDescriptions": [
            "%config.countBadge.all%",
            "%config.countBadge.tracked%",
            "%config.countBadge.off%",
        ],
        "description": "%config.countBadge%",
        "default": "all",
        "scope": "resource",
    },
    "git.checkoutType": {
        "type": "array",
        "items": {
            "type": "string",
            "enum": ["local", "tags", "remote"],
            "enumDescriptions": [
                "%config.checkoutType.local%",
                "%config.checkoutType.tags%",
                "%config.checkoutType.remote%",
            ],
        },
        "uniqueItems": true,
        "markdownDescription": "%config.checkoutType%",
        "default": ["local", "remote", "tags"],
    },
    "git.ignoreLegacyWarning": {
        "type": "boolean",
        "description": "%config.ignoreLegacyWarning%",
        "default": false,
    },
    "git.ignoreMissingGitWarning": {
        "type": "boolean",
        "description": "%config.ignoreMissingGitWarning%",
        "default": false,
    },
    "git.ignoreWindowsGit27Warning": {
        "type": "boolean",
        "description": "%config.ignoreWindowsGit27Warning%",
        "default": false,
    },
    "git.ignoreLimitWarning": {
        "type": "boolean",
        "description": "%config.ignoreLimitWarning%",
        "default": false,
    },
    "git.ignoreRebaseWarning": {
        "type": "boolean",
        "description": "%config.ignoreRebaseWarning%",
        "default": false,
    },
    "git.defaultCloneDirectory": {
        "type": ["string", "null"],
        "default": null,
        "scope": "machine",
        "description": "%config.defaultCloneDirectory%",
    },
    "git.useEditorAsCommitInput": {
        "type": "boolean",
        "description": "%config.useEditorAsCommitInput%",
        "default": true,
    },
    "git.verboseCommit": {
        "type": "boolean",
        "scope": "resource",
        "markdownDescription": "%config.verboseCommit%",
        "default": false,
    },
    "git.enableSmartCommit": {
        "type": "boolean",
        "scope": "resource",
        "description": "%config.enableSmartCommit%",
        "default": false,
    },
    "git.smartCommitChanges": {
        "type": "string",
        "enum": ["all", "tracked"],
        "enumDescriptions": [
            "%config.smartCommitChanges.all%",
            "%config.smartCommitChanges.tracked%",
        ],
        "scope": "resource",
        "description": "%config.smartCommitChanges%",
        "default": "all",
    },
    "git.suggestSmartCommit": {
        "type": "boolean",
        "scope": "resource",
        "description": "%config.suggestSmartCommit%",
        "default": true,
    },
    "git.enableCommitSigning": {
        "type": "boolean",
        "scope": "resource",
        "description": "%config.enableCommitSigning%",
        "default": false,
    },
    "git.confirmEmptyCommits": {
        "type": "boolean",
        "scope": "resource",
        "description": "%config.confirmEmptyCommits%",
        "default": true,
    },
    "git.decorations.enabled": {
        "type": "boolean",
        "default": true,
        "description": "%config.decorations.enabled%",
    },
    "git.enableStatusBarSync": {
        "type": "boolean",
        "default": true,
        "description": "%config.enableStatusBarSync%",
        "scope": "resource",
    },
    "git.followTagsWhenSync": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.followTagsWhenSync%",
    },
    "git.promptToSaveFilesBeforeStash": {
        "type": "string",
        "enum": ["always", "staged", "never"],
        "enumDescriptions": [
            "%config.promptToSaveFilesBeforeStash.always%",
            "%config.promptToSaveFilesBeforeStash.staged%",
            "%config.promptToSaveFilesBeforeStash.never%",
        ],
        "scope": "resource",
        "default": "always",
        "description": "%config.promptToSaveFilesBeforeStash%",
    },
    "git.promptToSaveFilesBeforeCommit": {
        "type": "string",
        "enum": ["always", "staged", "never"],
        "enumDescriptions": [
            "%config.promptToSaveFilesBeforeCommit.always%",
            "%config.promptToSaveFilesBeforeCommit.staged%",
            "%config.promptToSaveFilesBeforeCommit.never%",
        ],
        "scope": "resource",
        "default": "always",
        "description": "%config.promptToSaveFilesBeforeCommit%",
    },
    "git.postCommitCommand": {
        "type": "string",
        "enum": ["none", "push", "sync"],
        "enumDescriptions": [
            "%config.postCommitCommand.none%",
            "%config.postCommitCommand.push%",
            "%config.postCommitCommand.sync%",
        ],
        "markdownDescription": "%config.postCommitCommand%",
        "scope": "resource",
        "default": "none",
    },
    "git.openAfterClone": {
        "type": "string",
        "enum": ["always", "alwaysNewWindow", "whenNoFolderOpen", "prompt"],
        "enumDescriptions": [
            "%config.openAfterClone.always%",
            "%config.openAfterClone.alwaysNewWindow%",
            "%config.openAfterClone.whenNoFolderOpen%",
            "%config.openAfterClone.prompt%",
        ],
        "default": "prompt",
        "description": "%config.openAfterClone%",
    },
    "git.showInlineOpenFileAction": {
        "type": "boolean",
        "default": true,
        "description": "%config.showInlineOpenFileAction%",
    },
    "git.showPushSuccessNotification": {
        "type": "boolean",
        "description": "%config.showPushSuccessNotification%",
        "default": false,
    },
    "git.inputValidation": {
        "type": "string",
        "enum": ["always", "warn", "off"],
        "default": "warn",
        "description": "%config.inputValidation%",
    },
    "git.inputValidationLength": {
        "type": "number",
        "default": 72,
        "description": "%config.inputValidationLength%",
    },
    "git.inputValidationSubjectLength": {
        "type": ["number", "null"],
        "default": 50,
        "description": "%config.inputValidationSubjectLength%",
    },
    "git.detectSubmodules": {
        "type": "boolean",
        "scope": "resource",
        "default": true,
        "description": "%config.detectSubmodules%",
    },
    "git.detectSubmodulesLimit": {
        "type": "number",
        "scope": "resource",
        "default": 10,
        "description": "%config.detectSubmodulesLimit%",
    },
    "git.alwaysShowStagedChangesResourceGroup": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.alwaysShowStagedChangesResourceGroup%",
    },
    "git.alwaysSignOff": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.alwaysSignOff%",
    },
    "git.ignoreSubmodules": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.ignoreSubmodules%",
    },
    "git.ignoredRepositories": {
        "type": "array",
        "items": {"type": "string"},
        "default": [],
        "scope": "window",
        "description": "%config.ignoredRepositories%",
    },
    "git.scanRepositories": {
        "type": "array",
        "items": {"type": "string"},
        "default": [],
        "scope": "resource",
        "description": "%config.scanRepositories%",
    },
    "git.showProgress": {
        "type": "boolean",
        "description": "%config.showProgress%",
        "default": true,
        "scope": "resource",
    },
    "git.rebaseWhenSync": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.rebaseWhenSync%",
    },
    "git.fetchOnPull": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.fetchOnPull%",
    },
    "git.pruneOnFetch": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.pruneOnFetch%",
    },
    "git.pullTags": {
        "type": "boolean",
        "scope": "resource",
        "default": true,
        "description": "%config.pullTags%",
    },
    "git.autoStash": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.autoStash%",
    },
    "git.allowForcePush": {
        "type": "boolean",
        "default": false,
        "description": "%config.allowForcePush%",
    },
    "git.useForcePushWithLease": {
        "type": "boolean",
        "default": true,
        "description": "%config.useForcePushWithLease%",
    },
    "git.confirmForcePush": {
        "type": "boolean",
        "default": true,
        "description": "%config.confirmForcePush%",
    },
    "git.allowNoVerifyCommit": {
        "type": "boolean",
        "default": false,
        "description": "%config.allowNoVerifyCommit%",
    },
    "git.confirmNoVerifyCommit": {
        "type": "boolean",
        "default": true,
        "description": "%config.confirmNoVerifyCommit%",
    },
    "git.closeDiffOnOperation": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.closeDiffOnOperation%",
    },
    "git.openDiffOnClick": {
        "type": "boolean",
        "scope": "resource",
        "default": true,
        "description": "%config.openDiffOnClick%",
    },
    "git.supportCancellation": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.supportCancellation%",
    },
    "git.branchSortOrder": {
        "type": "string",
        "enum": ["committerdate", "alphabetically"],
        "default": "committerdate",
        "description": "%config.branchSortOrder%",
    },
    "git.untrackedChanges": {
        "type": "string",
        "enum": ["mixed", "separate", "hidden"],
        "enumDescriptions": [
            "%config.untrackedChanges.mixed%",
            "%config.untrackedChanges.separate%",
            "%config.untrackedChanges.hidden%",
        ],
        "default": "mixed",
        "description": "%config.untrackedChanges%",
        "scope": "resource",
    },
    "git.requireGitUserConfig": {
        "type": "boolean",
        "description": "%config.requireGitUserConfig%",
        "default": true,
        "scope": "resource",
    },
    "git.showCommitInput": {
        "type": "boolean",
        "scope": "resource",
        "default": true,
        "description": "%config.showCommitInput%",
    },
    "git.terminalAuthentication": {
        "type": "boolean",
        "default": true,
        "description": "%config.terminalAuthentication%",
    },
    "git.terminalGitEditor": {
        "type": "boolean",
        "default": false,
        "description": "%config.terminalGitEditor%",
    },
    "git.useCommitInputAsStashMessage": {
        "type": "boolean",
        "scope": "resource",
        "default": false,
        "description": "%config.useCommitInputAsStashMessage%",
    },
    "git.useIntegratedAskPass": {
        "type": "boolean",
        "default": true,
        "description": "%config.useIntegratedAskPass%",
    },
    "git.githubAuthentication": {
        "deprecationMessage": "This setting is now deprecated, please use `github.gitAuthentication` instead."
    },
    "git.timeline.date": {
        "type": "string",
        "enum": ["committed", "authored"],
        "enumDescriptions": [
            "%config.timeline.date.committed%",
            "%config.timeline.date.authored%",
        ],
        "default": "committed",
        "description": "%config.timeline.date%",
        "scope": "window",
    },
    "git.timeline.showAuthor": {
        "type": "boolean",
        "default": true,
        "description": "%config.timeline.showAuthor%",
        "scope": "window",
    },
    "git.timeline.showUncommitted": {
        "type": "boolean",
        "default": false,
        "description": "%config.timeline.showUncommitted%",
        "scope": "window",
    },
    "git.showActionButton": {
        "type": "object",
        "additionalProperties": false,
        "description": "%config.showActionButton%",
        "properties": {
            "commit": {
                "type": "boolean",
                "description": "%config.showActionButton.commit%",
            },
            "publish": {
                "type": "boolean",
                "description": "%config.showActionButton.publish%",
            },
            "sync": {
                "type": "boolean",
                "description": "%config.showActionButton.sync%",
            },
        },
        "default": {"commit": true, "publish": true, "sync": true},
        "scope": "resource",
    },
    "git.statusLimit": {
        "type": "number",
        "scope": "resource",
        "default": 10000,
        "description": "%config.statusLimit%",
    },
    "git.repositoryScanIgnoredFolders": {
        "type": "array",
        "items": {"type": "string"},
        "default": ["node_modules"],
        "scope": "resource",
        "markdownDescription": "%config.repositoryScanIgnoredFolders%",
    },
    "git.repositoryScanMaxDepth": {
        "type": "number",
        "scope": "resource",
        "default": 1,
        "markdownDescription": "%config.repositoryScanMaxDepth%",
    },
    "git.commandsToLog": {
        "type": "array",
        "items": {"type": "string"},
        "default": [],
        "markdownDescription": "%config.commandsToLog%",
    },
    "git.logLevel": {
        "type": "string",
        "default": "Info",
        "enum": ["Trace", "Debug", "Info", "Warning", "Error", "Critical", "Off"],
        "enumDescriptions": [
            "%config.logLevel.trace%",
            "%config.logLevel.debug%",
            "%config.logLevel.info%",
            "%config.logLevel.warn%",
            "%config.logLevel.error%",
            "%config.logLevel.critical%",
            "%config.logLevel.off%",
        ],
        "markdownDescription": "%config.logLevel%",
        "scope": "window",
    },
    "git.mergeEditor": {
        "type": "boolean",
        "default": true,
        "markdownDescription": "%config.mergeEditor%",
        "scope": "window",
    },
}


class MyObject:
    def __init__(self, name: str, schema):
        self.name = name
        self.schema = schema
        self.cfg = ConfigurationProperty(**schema)

    def __str__(self):
        return self.name

    @property
    def category(self):
        splits = self.name.split(".")
        return " \u203a ".join(_split_camel(s) for s in splits[:-1]) + ": "

    @property
    def label(self) -> str:
        return _split_camel(self.name.rsplit(".", 1)[-1])


class AbstractSettingRenderer(ABC):
    LEFT_PAD = 5
    TOP_PAD = 5

    @abstractmethod
    def paintElement(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        ...

    @abstractmethod
    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        ...

    def _category_and_label(self, item: MyObject) -> Tuple[str, str]:
        splits = item.name.split(".")
        category = " \u203a ".join(_split_camel(s) for s in splits[:-1]) + ": "
        label = _split_camel(splits[-1])
        return category, label

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        editor = self.getEditorWidget(parent, option, index)
        # editor.setProperty("setting")
        if editor is not None:
            editor.setGeometry(option.rect)
        return editor

    def _drawDescription(self, painter: QPainter, rect, item: MyObject, option):
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft, item.cfg.description)

    def paintCommon(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        item: MyObject = index.data(Qt.ItemDataRole.UserRole)
        category, label = self._category_and_label(item)

        font = painter.font()
        fm = QFontMetrics(font)

        category_rect = option.rect.translated(self.LEFT_PAD, self.TOP_PAD)
        label_rect = category_rect.translated(fm.width(category), 0)
        painter.drawText(category_rect, Qt.AlignmentFlag.AlignLeft, category)

        font.setBold(True)  # TODO: use stylesheet
        painter.setFont(font)
        painter.drawText(label_rect, Qt.AlignmentFlag.AlignLeft, label)
        font.setBold(False)
        painter.setFont(font)

        rect = category_rect.translated(0, fm.height() + 5)
        self._drawDescription(painter, rect, item, option)

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        self.paintCommon(painter, option, index)
        self.paintElement(painter, option, index)

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        return False


class SettingComplexRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        ...


class SettingArrayRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        ...


class SettingObjectRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        ...


class SettingExcludeRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        ...


class SettingTextRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        return QLineEdit(parent)


class SettingMultilineTextRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        return QTextEdit(parent)


class SettingEnumRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        return QComboBox(parent)


class SettingNumberRenderer(AbstractSettingRenderer):
    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        return QDoubleSpinBox(parent)


class SettingBoolRenderer(AbstractSettingRenderer):
    def _drawDescription(self, painter, rect: QRect, item: MyObject, option):
        checked = Qt.CheckState.Checked if item.cfg.default else Qt.CheckState.Unchecked

        self.drawCheck(painter, option, checked)
        check_width = 22  # TODO
        super()._drawDescription(painter, rect.translated(check_width, 0), item, option)

    def paintElement(self, painter, option, index):
        ...

    def getEditorWidget(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        ...

    def drawCheck(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        state: Qt.CheckState,
    ) -> None:
        if not option.rect.isValid():
            return

        if state == Qt.CheckState.Checked:
            option.state |= QStyle.StateFlag.State_On
        elif state == Qt.CheckState.PartiallyChecked:
            option.state |= QStyle.StateFlag.State_NoChange
        else:
            option.state |= QStyle.StateFlag.State_Off

        option.rect.translate(5, 7)  # WHY?  # TODO
        check = QStyle.PrimitiveElement.PE_IndicatorItemViewItemCheck
        QApplication.style().drawPrimitive(check, option, painter, option.widget)

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        if event.type() == QEvent.Type.MouseButtonPress:
            print("toggle!")
        return super().editorEvent(event, model, option, index)


class SettingDelegate(QAbstractItemDelegate):
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._renderers = {
            "object": SettingObjectRenderer(),
            "boolean": SettingBoolRenderer(),
            "number": SettingNumberRenderer(),
            "string": SettingTextRenderer(),
            "array": SettingArrayRenderer(),
            "enum": SettingEnumRenderer(),
            "exclude": SettingExcludeRenderer(),
            "complex": SettingComplexRenderer(),
        }

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(300, 70)

    def renderer_for(self, index: QModelIndex) -> AbstractSettingRenderer:
        item: MyObject = index.data(Qt.ItemDataRole.UserRole)
        json_type = "enum" if item.cfg.enum else item.cfg.type
        if isinstance(json_type, list):
            json_type = json_type[0]  # TODO: handle Union types better
        return self._renderers[json_type]

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        self.renderer_for(index).paint(painter, option, index)

    def createEditor(
        self, parent: QWidget, option: "QStyleOptionViewItem", index: QModelIndex
    ) -> QWidget:
        return self.renderer_for(index).createEditor(parent, option, index)

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        return self.renderer_for(index).editorEvent(event, model, option, index)

    def setEditorData(self, editor: QWidget, index) -> None:
        item: MyObject = index.data(Qt.ItemDataRole.UserRole)
        if item.cfg.enum:
            for item in item.cfg.enum:
                editor.addItem(str(item), item)
        elif item.cfg.type == "boolean":
            editor.setChecked(item.cfg.default)
        elif item.cfg.type == "string":
            editor.setText(item.cfg.default)
        elif item.cfg.type in {"number", "integer"}:
            editor.setValue(item.cfg.default)


root = SelectableEventedList([MyObject(k, v) for k, v in properties.items()])
view = QtListView(root)
view.setEditTriggers(QtListView.EditTrigger.AllEditTriggers)
view.setDragEnabled(False)
view.setItemDelegate(SettingDelegate())
view.show()


napari.run()
