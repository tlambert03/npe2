from qtpy.QtCore import QEvent, QModelIndex, Qt, Signal
from qtpy.QtGui import QStandardItemModel
from qtpy.QtWidgets import (
    QComboBox,
    QFrame,
    QItemDelegate,
    QListView,
    QVBoxLayout,
    QWidget,
)


class Delegate(QItemDelegate):
    indexHovered = Signal(QModelIndex)

    def paint(self, painter, option, index) -> None:
        super().paint(painter, option, index)
        if index.row() == 1:
            painter.save()
            painter.setPen(Qt.GlobalColor.blue)
            painter.drawText(
                option.rect.adjusted(0, 0, -10, 0),
                Qt.AlignmentFlag.AlignRight,
                "default",
            )
            painter.restore()

    def editorEvent(self, event, model, option, index) -> bool:
        if event.type() == QEvent.Type.MouseMove:
            self.indexHovered.emit(index)
        return super().editorEvent(event, model, option, index)


class CustomView(QListView):
    ...


class CustomModel(QStandardItemModel):
    ...
    # def index(self, row: int, column: int, parent):
    #     return super().index(row, column, parent)

    # def parent(self, index):
    #     print("parent", index.row())
    #     return super().parent(index)

    def rowCount(self, parent_index) -> int:
        print("rowCount", parent_index.row())
        return super().rowCount(parent_index)

    # def data(self, index, role):
    #     if index.row() == 3:
    #         print("HI")
    #         index = self.index(index.row() - 1, 0, index.parent())
    #         return super().data(index, role)
    #     print("data", index.row(), role)
    #     return super().data(index, role)


class ComboDescript(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setModel(CustomModel())
        # self.setView(CustomView())
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        delegate = Delegate()
        self.setItemDelegate(delegate)
        delegate.indexHovered.connect(self.on_index_hovered)
        self.addItems(["a", "b", "c"])
        self.currentIndexChanged.connect(self.on_index_changed)
        self.setMinimumWidth(200)
        self.addItem("one")
        self._set_last_row_hidden(True)

    def on_index_changed(self, index):
        print("index changed to", index)
        print("text is", self.itemText(index))

    def on_index_hovered(self, index):
        self._set_last_row_hidden(index.row() == 0)

    def _set_last_row_hidden(self, hidden):
        self.view().setRowHidden(self.count() - 1, hidden)
        self.setMaxVisibleItems(10)

    def showPopup(self) -> None:
        super().showPopup()
        frame: QFrame = self.findChild(QFrame)
        topleft = self.mapToGlobal(frame.rect().topLeft())
        topleft.setY(topleft.y() + self.height() - 6)
        topleft.setX(topleft.x() + 6)
        frame.move(topleft)


# app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
w = ComboDescript()
layout.addWidget(w)
window.setLayout(layout)
window.show()
# sys.exit(app.exec_())
