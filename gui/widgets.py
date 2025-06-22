from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class ScriptScopeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScriptScope GUI")
        self.resize(900, 500)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Script Name", "PID", "CPU (%)", "MEM (%)", "Elapsed Time", "Command"]
        )
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # TODO: Ajouter boutons, menu, logique de rafraîchissement, etc.
