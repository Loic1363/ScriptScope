import os
import json
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

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

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(1000)  # Refresh every second

        self.refresh_table()  # Initial load

    def refresh_table(self):
        # Always look for stats.json at the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stats_path = os.path.join(project_root, "stats.json")
        try:
            with open(stats_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            data = []
        self.table.setRowCount(len(data))
        for row, entry in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(entry.get("script_name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry.get("pid", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(entry.get("cpu", ""))))
            self.table.setItem(row, 3, QTableWidgetItem(str(entry.get("mem", ""))))
            self.table.setItem(row, 4, QTableWidgetItem(entry.get("etime", "")))
            self.table.setItem(row, 5, QTableWidgetItem(entry.get("cmd", "")))
