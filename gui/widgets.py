import os
import json
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QAction
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor

class ScriptScopeMainWindow(QMainWindow):
    """
    ================================================================================
    ScriptScopeMainWindow Class Definition
    Main window for the ScriptScope GUI application.
    ================================================================================
    """
    COLUMNS = [
        ("Script Name", 180),
        ("PID", 80),
        ("CPU (%)", 80),
        ("CPU Total (%)", 100),
        ("MEM (%)", 80),
        ("Elapsed Time", 120),
        ("Command", 280)
    ]

    def __init__(self):
        """
        ================================================================================
        Initialization: Setup window, menu, table, and timer.
        ================================================================================
        """
        super().__init__()
        self.setWindowTitle("ScriptScope GUI")
        self.resize(900, 500)
        self.last_data = []
        self.has_shown_waiting = False

        self._init_menu()
        self._init_table()
        self._init_timer()

    def _init_menu(self):
        """
        ================================================================================
        Menu Bar Initialization: Add column visibility toggles.
        ================================================================================
        """
        menu = self.menuBar().addMenu("Select")
        self.column_actions = {}
        for idx, (name, _) in enumerate(self.COLUMNS):
            action = QAction(name, self, checkable=True, checked=True)
            action.triggered.connect(lambda checked, c=idx: self.toggle_column_visibility(c, checked))
            menu.addAction(action)
            self.column_actions[idx] = action

    def _init_table(self):
        """
        ================================================================================
        Table Widget Initialization: Setup columns and layout.
        ================================================================================
        """
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels([name for name, _ in self.COLUMNS])
        self.table.setAlternatingRowColors(True)
        for idx, (_, width) in enumerate(self.COLUMNS):
            self.table.setColumnWidth(idx, width)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _init_timer(self):
        """
        ================================================================================
        Timer Initialization: Periodically refresh table data.
        ================================================================================
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(1000)
        self.refresh_table()

    def toggle_column_visibility(self, column, visible):
        """
        ================================================================================
        Toggle Column Visibility: Show or hide table columns.
        ================================================================================
        """
        (self.table.showColumn if visible else self.table.hideColumn)(column)

    def refresh_table(self):
        """
        ================================================================================
        Table Refresh: Load data from stats.json and update table.
        ================================================================================
        """
        stats_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "stats.json"
        )
        try:
            with open(stats_path, "r") as f:
                data = json.load(f)
        except Exception:
            data = []

        if not data and not self.last_data and not self.has_shown_waiting:
            self.table.setRowCount(1)
            item = QTableWidgetItem("Waiting for data...")
            item.setForeground(QColor("#ffcc00"))
            self.table.setItem(0, 0, item)
            for col in range(1, len(self.COLUMNS)):
                self.table.setItem(0, col, QTableWidgetItem(""))
            self.has_shown_waiting = True
            return

        if data:
            self.last_data = data
            self.has_shown_waiting = False
            self.update_table(data)

    def update_table(self, data):
        """
        ================================================================================
        Update Table: Populate table rows from loaded data.
        ================================================================================
        """
        self.table.setRowCount(len(data))
        for row, entry in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(entry.get("script_name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry.get("pid", ""))))

            cpu = self._safe_float(entry.get("cpu", "0"))
            cpu_item = QTableWidgetItem(f"{cpu:.2f}")
            cpu_item.setForeground(QColor("red") if cpu >= 10 else QColor("green"))
            self.table.setItem(row, 2, cpu_item)

            cpu_total = self._safe_div(cpu, os.cpu_count())
            cpu_total_item = QTableWidgetItem(f"{cpu_total:.2f}")
            cpu_total_item.setForeground(QColor("red") if cpu_total >= 10 else QColor("green"))
            self.table.setItem(row, 3, cpu_total_item)

            mem = self._safe_float(entry.get("mem", "0"))
            mem_item = QTableWidgetItem(f"{mem:.2f}")
            mem_item.setForeground(QColor("red") if mem >= 10 else QColor("green"))
            self.table.setItem(row, 4, mem_item)

            self.table.setItem(row, 5, QTableWidgetItem(entry.get("etime", "")))
            self.table.setItem(row, 6, QTableWidgetItem(entry.get("cmd", "")))

    @staticmethod
    def _safe_float(value):
        """
        ================================================================================
        Utility Function: Safe float conversion.
        ================================================================================
        """
        try:
            return float(value)
        except Exception:
            return 0.0

    @staticmethod
    def _safe_div(num, denom):
        """
        ================================================================================
        Utility Function: Safe division.
        ================================================================================
        """
        try:
            return round(num / denom, 2) if denom else 0.0
        except Exception:
            return 0.0
