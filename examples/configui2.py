import re

import napari
from napari.qt import get_app
from qtpy.QtWidgets import (
    QCheckBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from npe2.manifest.contributions import ConfigurationProperty

splitter = re.compile(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)")


def _split_camel(identifier: str) -> str:
    return " ".join([m.group(0).capitalize() for m in splitter.finditer(identifier)])


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


get_app()
true = True
false = False
null = None

properties = {
    "git.enabled": {
        "type": "boolean",
        "scope": "resource",
        "description": "Whether git is enabled.",
        "default": true,
    },
    "git.path": {
        "type": ["string", "null", "array"],
        "markdownDescription": "Path and filename of the git executable, e.g. `C:\\Program Files\\Git\\bin\\git.exe` (Windows). This can also be an array of string values containing multiple paths to look up.",
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
        "markdownDescription": "When set to [true](https://www.google.com), commits will automatically be fetched from the default remote of the current Git repository. Setting to `all` will fetch from all remotes.",
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


from magicgui.widgets import ComboBox, EmptyWidget, create_widget
from markdown_it import MarkdownIt

md = MarkdownIt()


def widget_for(obj: MyObject):
    wdg = QWidget()
    wdg.setLayout(QVBoxLayout())
    wdg.layout().setSpacing(0)
    title = QLabel(f"{obj.category}<strong>{obj.label}</strong>")
    title.setToolTip(obj.name)
    wdg.layout().addWidget(title)
    if obj.cfg.markdown_description:
        description = md.render(obj.cfg.markdown_description)
    else:
        description = obj.cfg.description

    if obj.cfg.type == "boolean":
        wdg.layout().addWidget(QCheckBox(description))
    else:
        if description:
            lbl = QLabel(description)
            lbl.setWordWrap(True)
            lbl.setOpenExternalLinks(True)
            wdg.layout().addWidget(lbl)

        hint = obj.cfg.python_type
        if hint is list or isinstance(hint, list):
            return wdg

        if obj.cfg.enum:
            editor = ComboBox(choices=obj.cfg.enum, value=obj.cfg.default)
        else:
            editor = create_widget(
                value=obj.cfg.default, name=obj.name, annotation=hint
            )
        if not isinstance(editor, EmptyWidget):
            wdg.layout().addWidget(editor.native)

    return wdg


wdg = QListWidget()
for item in properties.items():
    obj = MyObject(*item)
    wdg_item = QListWidgetItem()
    wdg.addItem(wdg_item)
    obj_wdg = widget_for(obj)
    wdg_item.setSizeHint(obj_wdg.sizeHint())
    wdg.setItemWidget(wdg_item, obj_wdg)

wdg.show()

napari.run()
