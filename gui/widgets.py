import os
import json
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem,
                            QVBoxLayout, QWidget, QMenuBar, QMenu, QAction)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QColor

class ScriptScopeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScriptScope GUI")
        self.resize(900, 500)
        # self.setWindowIcon(QIcon("icon.png"))  # Optionnel

        # Crée la barre de menus
        self.create_menu_bar()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Script Name", "PID", "CPU (%)", "CPU Total (%)", "MEM (%)", "Elapsed Time", "Command"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 280)

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

    def create_menu_bar(self):
        # Crée la barre de menus
        menu_bar = self.menuBar()
        select_menu = menu_bar.addMenu("Select")

        # Liste des colonnes et de leur index
        self.column_visibility = {
            "Script Name": 0,
            "PID": 1,
            "CPU (%)": 2,
            "CPU Total (%)": 3,
            "MEM (%)": 4,
            "Elapsed Time": 5,
            "Command": 6
        }

        # Ajoute une action pour chaque colonne (case à cocher)
        self.column_actions = {}
        for name, col in self.column_visibility.items():
            action = QAction(name, self, checkable=True, checked=True)
            action.triggered.connect(lambda checked, c=col: self.toggle_column_visibility(c, checked))
            select_menu.addAction(action)
            self.column_actions[col] = action

    def toggle_column_visibility(self, column, visible):
        if visible:
            self.table.showColumn(column)
        else:
            self.table.hideColumn(column)

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
            for col in range(1, 7):
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
            # CPU par cœur
            cpu_str = entry.get("cpu", "0")
            try:
                cpu = round(float(cpu_str), 2)
            except ValueError:
                cpu = 0.0
            self.table.setItem(row, 2, QTableWidgetItem(str(cpu)))
            # CPU total (relatif)
            cpu_total = round(cpu / os.cpu_count(), 2)
            self.table.setItem(row, 3, QTableWidgetItem(str(cpu_total)))
            # Mem
            mem_str = entry.get("mem", "0")
            try:
                mem = round(float(mem_str), 2)
            except ValueError:
                mem = 0.0
            self.table.setItem(row, 4, QTableWidgetItem(str(mem)))
            self.table.setItem(row, 5, QTableWidgetItem(entry.get("etime", "")))
            self.table.setItem(row, 6, QTableWidgetItem(entry.get("cmd", "")))
