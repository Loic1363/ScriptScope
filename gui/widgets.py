import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QAction, QFrame, QMenu, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

PRIMARY_COLOR = "#0bda5e"
DANGER_COLOR = "#fa6238"
BACKGROUND = "#111418"
BORDER_COLOR = "#3b4754"
TEXT_COLOR = "#fff"
SECONDARY_TEXT = "#9caaba"
FONT_FAMILY = "Inter, 'Noto Sans', sans-serif"

TABLE_STYLE = """
QTableWidget {
    background-color: #121416;
    color: #f3f4f6;
    border: 1.5px solid #40474f;
    border-radius: 16px;
    font-family: Inter, 'Noto Sans', sans-serif;
    font-size: 15px;
    gridline-color: #40474f;
    selection-background-color: #232a33;
    selection-color: #fff;
    outline: none;
}
QHeaderView::section {
    background-color: #1e2124;
    color: #fff;
    font-weight: 700;
    font-size: 15px;
    border: none;
    border-bottom: 2px solid #40474f;
    padding: 18px 24px;
    letter-spacing: -0.01em;
}
QTableWidget::item {
    background: transparent;
    padding: 18px 24px;
    border: none;
    border-bottom: 1px solid #40474f;
}
QTableWidget::item:selected {
    background-color: #232a33;
    color: #fff;
}
QTableCornerButton::section {
    background-color: #1e2124;
    border: none;
}
"""

class MetricCard(QFrame):
    def __init__(self, title, value, subtitle, change, color=PRIMARY_COLOR):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BACKGROUND};
                border: 1.5px solid {BORDER_COLOR};
                border-radius: 16px;
                padding: 18px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.10);
            }}
            QLabel {{
                font-family: {FONT_FAMILY};
            }}
        """)
        layout = QVBoxLayout(self)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 15px; font-weight: 600;")
        value_lbl = QLabel(value)
        value_lbl.setStyleSheet(f"color: {TEXT_COLOR}; font-size: 34px; font-weight: bold;")
        subtitle_layout = QHBoxLayout()
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 13px;")
        change_lbl = QLabel(change)
        change_lbl.setStyleSheet(f"color: {color}; font-size: 13px; font-weight: 600;")
        subtitle_layout.addWidget(subtitle_lbl)
        subtitle_layout.addWidget(change_lbl)
        subtitle_layout.addStretch()
        layout.addWidget(title_lbl)
        layout.addWidget(value_lbl)
        layout.addLayout(subtitle_layout)
        layout.addStretch()

class ScriptScopeMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScriptScope Dashboard")
        self.resize(1200, 900)
        self.setStyleSheet(f"background-color: {BACKGROUND}; font-family: {FONT_FAMILY};")
        self.init_column_menu_actions()

        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        logo = QLabel("🟦")
        logo.setStyleSheet("font-size: 24px;")
        title = QLabel("ScriptScope")
        title.setStyleSheet(f"color: {TEXT_COLOR}; font-size: 22px; font-weight: bold;")
        header_layout.addWidget(logo)
        header_layout.addWidget(title)
        header_layout.addStretch()

        nav_layout = QHBoxLayout()
        self.select_nav_btn = QPushButton("Select")
        self.select_nav_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {TEXT_COLOR};
                border: none;
                font-size: 15px;
                font-weight: 500;
                padding: 0 12px;
            }}
            QPushButton:hover {{
                color: {PRIMARY_COLOR};
                text-decoration: underline;
            }}
        """)
        self.select_nav_btn.setCursor(Qt.PointingHandCursor)
        self.select_nav_btn.clicked.connect(self.show_select_menu)
        nav_layout.addWidget(self.select_nav_btn)
        for label in ["Dashboard", "Scripts", "Paramètres"]:
            nav_btn = QLabel(label)
            nav_btn.setStyleSheet(f"color: {TEXT_COLOR}; font-size: 15px; font-weight: 500; padding: 0 12px;")
            nav_layout.addWidget(nav_btn)

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        header_layout.addWidget(nav_widget)

        avatar = QLabel()
        avatar.setFixedSize(40, 40)
        avatar.setStyleSheet(f"border-radius: 20px; background: {BORDER_COLOR};")
        header_layout.addWidget(avatar)

        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        main_layout.addWidget(header_widget)

        overview_layout = QVBoxLayout()
        overview_title = QLabel("Project Overview")
        overview_title.setStyleSheet(f"color: {TEXT_COLOR}; font-size: 32px; font-weight: bold;")
        overview_sub = QLabel("Analyse des scripts et ressources système")
        overview_sub.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 15px;")
        overview_layout.addWidget(overview_title)
        overview_layout.addWidget(overview_sub)
        overview_layout.setSpacing(0)
        overview_layout.setContentsMargins(30, 20, 0, 0)
        main_layout.addLayout(overview_layout)

        cards_layout = QHBoxLayout()
        cards_layout.setContentsMargins(30, 40, 30, 0)
        cards_layout.setSpacing(25)
        cards_layout.addWidget(MetricCard("CPU Usage", "65%", "7 derniers jours", "+5%", PRIMARY_COLOR))
        cards_layout.addWidget(MetricCard("RAM Usage", "78%", "7 derniers jours", "-2%", DANGER_COLOR))
        cards_layout.addWidget(MetricCard("Scripts actifs", "3", "en cours", "+1", PRIMARY_COLOR))
        main_layout.addLayout(cards_layout)

        section = QLabel("Performance des scripts")
        section.setStyleSheet(f"color: {TEXT_COLOR}; font-size: 22px; font-weight: bold; margin: 40px 0 10px 30px;")
        main_layout.addWidget(section)

        select_layout = QHBoxLayout()
        select_layout.setContentsMargins(30, 20, 30, 0)
        self.select_folder_btn = QPushButton("Choisir un dossier")
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.folder_label = QLabel("Dossier : aucun")
        self.folder_label.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 14px;")
        select_layout.addWidget(self.select_folder_btn)
        select_layout.addWidget(self.folder_label)
        self.select_file_btn = QPushButton("Choisir un fichier")
        self.select_file_btn.clicked.connect(self.select_file)
        self.file_label = QLabel("Fichier : aucun")
        self.file_label.setStyleSheet(f"color: {SECONDARY_TEXT}; font-size: 14px;")
        select_layout.addWidget(self.select_file_btn)
        select_layout.addWidget(self.file_label)
        select_layout.addStretch()
        main_layout.addLayout(select_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Script Name", "PID", "CPU (%)", "CPU Total (%)", "MEM (%)", "Elapsed Time", "Command"]
        )
        self.table.setAlternatingRowColors(False)
        self.table.setMinimumHeight(300)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        from PyQt5.QtWidgets import QHeaderView
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.setStyleSheet(TABLE_STYLE)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.last_data = []
        self.has_shown_waiting = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(1000)
        self.refresh_table()

    def init_column_menu_actions(self):
        self.column_visibility = {
            "Script Name": 0,
            "PID": 1,
            "CPU (%)": 2,
            "CPU Total (%)": 3,
            "MEM (%)": 4,
            "Elapsed Time": 5,
            "Command": 6
        }
        self.column_actions = {}
        for name, col in self.column_visibility.items():
            action = QAction(name, self, checkable=True, checked=True)
            action.triggered.connect(lambda checked, c=col: self.toggle_column_visibility(c, checked))
            self.column_actions[col] = action

    def show_select_menu(self):
        menu = QMenu()
        for col in self.column_visibility.values():
            menu.addAction(self.column_actions[col])
        menu.exec_(self.select_nav_btn.mapToGlobal(self.select_nav_btn.rect().bottomLeft()))

    def toggle_column_visibility(self, column, visible):
        if visible:
            self.table.showColumn(column)
        else:
            self.table.hideColumn(column)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if folder:
            self.folder_label.setText(f"Dossier : {folder}")

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier", "",
            "Tous les fichiers (*);;Scripts (*.sh *.py *.java)"
        )
        if file:
            self.file_label.setText(f"Fichier : {file}")

    def refresh_table(self):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        stats_path = os.path.join(project_root, "stats.json")
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
            cpu_str = entry.get("cpu", "0")
            try:
                cpu = float(cpu_str)
                cpu_item = QTableWidgetItem(f"{round(cpu, 2)}")
                cpu_item.setForeground(QColor("red") if cpu >= 10 else QColor("green"))
            except ValueError:
                cpu_item = QTableWidgetItem("0.0")
                cpu_item.setForeground(QColor("green"))
            self.table.setItem(row, 2, cpu_item)
            try:
                cpu_total = round(cpu / os.cpu_count(), 2)
                cpu_total_item = QTableWidgetItem(f"{cpu_total}")
                cpu_total_item.setForeground(QColor("red") if cpu_total >= 10 else QColor("green"))
            except Exception:
                cpu_total_item = QTableWidgetItem("0.0")
                cpu_total_item.setForeground(QColor("green"))
            self.table.setItem(row, 3, cpu_total_item)
            mem_str = entry.get("mem", "0")
            try:
                mem = float(mem_str)
                mem_item = QTableWidgetItem(f"{round(mem, 2)}")
                mem_item.setForeground(QColor("red") if mem >= 10 else QColor("green"))
            except ValueError:
                mem_item = QTableWidgetItem("0.0")
                mem_item.setForeground(QColor("green"))
            self.table.setItem(row, 4, mem_item)
            self.table.setItem(row, 5, QTableWidgetItem(entry.get("etime", "")))
            self.table.setItem(row, 6, QTableWidgetItem(entry.get("cmd", "")))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ScriptScopeMainWindow()
    window.show()
    sys.exit(app.exec_())
