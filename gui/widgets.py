import os
import json
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QColor

class ScriptScopeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScriptScope GUI")
        self.resize(900, 500)
        # self.setWindowIcon(QIcon("icon.png"))  # Optionnel

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Script Name", "PID", "CPU (%)", "MEM (%)", "Elapsed Time", "Command"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 280)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.last_data = []
        self.has_shown_waiting = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(1000)

        self.refresh_table()

    def refresh_table(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stats_path = os.path.join(project_root, "stats.json")
        try:
            with open(stats_path, "r") as f:
                data = json.load(f)
        except Exception as e:
            data = []

        if not data and not self.last_data and not self.has_shown_waiting:
            self.table.setRowCount(1)
            item = QTableWidgetItem("Waiting for data...")
            item.setForeground(QColor("#ffcc00"))
            self.table.setItem(0, 0, item)
            for col in range(1, 6):
                self.table.setItem(0, col, QTableWidgetItem(""))
            self.has_shown_waiting = True
            return

        if data:
            self.last_data = data
            self.has_shown_waiting = False
            self.update_table(data)

    def update_table(self, data):
        self.table.setRowCount(len(data))
        for row, entry in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(entry.get("script_name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry.get("pid", ""))))
            # Gestion de cpu
            cpu_str = entry.get("cpu", "0")
            try:
                cpu = round(float(cpu_str), 2)
            except ValueError:
                cpu = 0.0
            self.table.setItem(row, 2, QTableWidgetItem(str(cpu)))
            # Gestion de mem
            mem_str = entry.get("mem", "0")
            try:
                mem = round(float(mem_str), 2)
            except ValueError:
                mem = 0.0
            self.table.setItem(row, 3, QTableWidgetItem(str(mem)))
            self.table.setItem(row, 4, QTableWidgetItem(entry.get("etime", "")))
            self.table.setItem(row, 5, QTableWidgetItem(entry.get("cmd", "")))
