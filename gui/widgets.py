"""
===========================================================================================
ScriptScope GUI Application
-------------------------------------------------------------------------------------------
This module implements the main window for the ScriptScope GUI, a PyQt5-based application
designed to monitor and display real-time statistics about running scripts. The interface
provides a table view with customizable columns, periodic data refresh from a JSON file,
and visual indicators for CPU and memory usage. The code is organized into clearly
documented sections for maintainability and clarity.
===========================================================================================
"""

import os
import json

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtSvg import QSvgWidget

from PyQt5.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QSizePolicy,
    QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QFrame,
    QProgressBar
)

from .style import (
    apply_table_style, apply_mainwindow_style, style_button,
    style_title, style_separator, style_overview_title, style_overview_subtitle,
    style_metrics_rect, style_metrics_title, style_avg_time_label,
    style_script_label, style_script_progress_bar, style_no_scripts_label
)

SHOW_TABLE = False

class ScriptScopeMainWindow(QMainWindow):
    """
    ================================================================================
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
        super().__init__()
        self.setWindowTitle("ScriptScope GUI")
        self.resize(900, 500)
        self.last_data = []
        self.has_shown_waiting = False

        self.scripts_rect = None
        self.scripts_layout = None

        self._init_ui()
        self._init_timer()

        apply_mainwindow_style(self)

    def _init_ui(self):
        """
        ================================================================================
        Initialize the main UI components.
        ================================================================================
        """
        svg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pictures", "main.svg"))
        logo_widget = QSvgWidget(svg_path)
        logo_widget.setFixedSize(24, 24)

        title = QLabel("ScriptScope")
        style_title(title)

        title_logo_layout = QHBoxLayout()
        title_logo_layout.setContentsMargins(0, 0, 0, 0)
        title_logo_layout.setSpacing(8)
        title_logo_layout.addSpacing(20)
        title_logo_layout.addWidget(logo_widget)
        title_logo_layout.addWidget(title)
        title_logo_widget = QWidget()
        title_logo_widget.setLayout(title_logo_layout)

        avatar_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pictures", "default.svg"))
        avatar_widget = QSvgWidget(avatar_path)
        avatar_widget.setFixedSize(32, 32)

        self.select_btn = QPushButton("Select")
        self.dashboard_btn = QPushButton("Dashboard")
        self.projet_btn = QPushButton("Project")
        self.settings_btn = QPushButton("Settings")
        for btn in [self.select_btn, self.dashboard_btn, self.projet_btn, self.settings_btn]:
            style_button(btn)

        top_bar = QHBoxLayout()
        top_bar.addWidget(title_logo_widget)
        top_bar.addStretch(1)
        top_bar.addWidget(self.select_btn)
        top_bar.addWidget(self.dashboard_btn)
        top_bar.addWidget(self.projet_btn)
        top_bar.addWidget(self.settings_btn)
        top_bar.addSpacing(12)
        top_bar.addWidget(avatar_widget)
        top_bar.addSpacing(12)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        style_separator(separator)

        overview_container = QWidget()
        overview_container.setFixedWidth(900)

        overview_layout = QVBoxLayout()
        overview_layout.setContentsMargins(0, 0, 0, 0)
        overview_layout.setSpacing(0)

        overview_title = QLabel("Project Overview")
        overview_title.setAlignment(Qt.AlignLeft)
        style_overview_title(overview_title)

        overview_subtitle = QLabel(
            "A professional, modular Linux application for real-time monitoring and visualization of resource usage by project-specific scripts.\n"
            "ScriptScope helps developers and teams identify bottlenecks, optimize code, and maintain control over complex workflows."
        )
        overview_subtitle.setWordWrap(True)
        overview_subtitle.setAlignment(Qt.AlignLeft)
        style_overview_subtitle(overview_subtitle)

        overview_layout.addWidget(overview_title)
        overview_layout.addWidget(overview_subtitle)
        overview_container.setLayout(overview_layout)
        overview_layout.addSpacing(0)

        metrics_title = QLabel("Performance Metrics")
        metrics_title.setAlignment(Qt.AlignLeft)
        style_overview_title(metrics_title)
        overview_layout.addWidget(metrics_title)
        overview_layout.addSpacing(18)

        rect_width = 284
        rect_height = 400

        def create_metrics_rect(title_text):
            """
            ================================================================================
            Helper function: creates a styled metrics rectangle with a title.
            ================================================================================
            """
            rect = QFrame()
            rect.setFixedSize(rect_width, rect_height)
            style_metrics_rect(rect)
            rect.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            vbox = QVBoxLayout()
            vbox.setContentsMargins(16, 0, 16, 24)
            vbox.setSpacing(0)

            title = QLabel(title_text)
            style_metrics_title(title)
            title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            vbox.addWidget(title, alignment=Qt.AlignLeft | Qt.AlignTop)

            if title_text == "Script Execution Times":
                self.avg_time_label = QLabel("Average time: N/A")
                style_avg_time_label(self.avg_time_label)
                vbox.addWidget(self.avg_time_label)

                self.scripts_bar_container = QWidget()
                self.scripts_bar_layout = QVBoxLayout()
                self.scripts_bar_layout.setContentsMargins(0, 0, 0, 150)
                self.scripts_bar_layout.setSpacing(2)
                self.scripts_bar_container.setLayout(self.scripts_bar_layout)

                vbox.addWidget(self.scripts_bar_container, alignment=Qt.AlignTop)
                self.scripts_bar_container.setStyleSheet("border: none; background: transparent;")

                self.scripts_rect = rect
                self.scripts_layout = vbox
                self._update_scripts_rect()

            rect.setLayout(vbox)
            return rect

        rectangles_layout = QHBoxLayout()
        rectangles_layout.setContentsMargins(0, 0, 0, 0)
        rectangles_layout.setSpacing(24)

        titles = ["CPU Usage", "RAM Usage", "Script Execution Times"]
        for t in titles:
            rect = create_metrics_rect(t)
            rectangles_layout.addWidget(rect)

        rectangles_container = QWidget()
        rectangles_container.setLayout(rectangles_layout)
        rectangles_container.setFixedWidth(3 * rect_width + 2 * 24)

        overview_layout.addWidget(rectangles_container, alignment=Qt.AlignLeft)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.COLUMNS))
        self.table.setHorizontalHeaderLabels([name for name, _ in self.COLUMNS])
        self.table.setAlternatingRowColors(True)
        for idx, (_, width) in enumerate(self.COLUMNS):
            self.table.setColumnWidth(idx, width)
        apply_table_style(self.table)

        if not SHOW_TABLE:
            self.table.hide()
        else:
            self.table.show()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_bar)
        main_layout.addWidget(separator)
        main_layout.addWidget(overview_container, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.table)
        main_layout.addStretch(1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def _init_timer(self):
        """
        ================================================================================
        Initialize the timer for periodic data refresh.
        ================================================================================
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(1000)
        self.refresh_table()

    def toggle_column_visibility(self, column, visible):
        """
        ================================================================================
        Toggle the visibility of a table column.
        ================================================================================
        """
        (self.table.showColumn if visible else self.table.hideColumn)(column)

    def refresh_table(self):
        """
        ================================================================================
        Refresh table data from stats.json and update the metrics rectangle.
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
            if self.scripts_rect and self.scripts_layout:
                self._update_scripts_rect()

    def _update_scripts_rect(self):
        """
        ================================================================================
        Update the "Script Execution Times" rectangle with scripts and progress bars.
        Each bar represents the script execution time, normalized to the maximum time.
        ================================================================================
        """
        while self.scripts_bar_layout.count():
            item = self.scripts_bar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

        data = self.last_data
        scripts_with_times = []
        for entry in data:
            if "script_name" in entry and "etime" in entry:
                etime_str = entry["etime"]
                etime_sec = self.time_to_seconds(etime_str) if isinstance(etime_str, str) else int(etime_str)
                scripts_with_times.append((entry["script_name"], etime_sec))

        if not scripts_with_times:
            label = QLabel("No running scripts")
            style_no_scripts_label(label)
            self.scripts_bar_layout.addWidget(label)
        else:
            max_time = max(t for _, t in scripts_with_times) if scripts_with_times else 1
            if max_time == 0:
                max_time = 1
            for name, time_sec in scripts_with_times:
                hbox = QHBoxLayout()
                hbox.setContentsMargins(0, 8, 0, 8) #espace entre chaque barre
                hbox.setSpacing(20) #taille de la barre

                label_name = QLabel(name)
                style_script_label(label_name)
                hbox.addWidget(label_name)

                bar = QProgressBar()
                bar.setMaximum(100)
                bar.setValue(int((time_sec / max_time) * 100))
                bar.setTextVisible(False)
                style_script_progress_bar(bar)
                hbox.addWidget(bar, stretch=1)

                self.scripts_bar_layout.addLayout(hbox)

        common_style = (
            "color:#fff; "
            "font-size:24px; "
            "font-family:'Inter','Noto Sans',sans-serif; "
            "font-weight:bold; "
            "padding-left:8px; "
            "padding-top:2px;"
        )

        if hasattr(self, 'avg_time_label') and self.avg_time_label is not None:
            if scripts_with_times:
                avg_time_ms = sum(t * 1000 for _, t in scripts_with_times) / len(scripts_with_times)
                if avg_time_ms >= 10000:
                    valeur = f"{avg_time_ms / 1000:.1f}"
                    unite = "s"
                else:
                    valeur = f"{avg_time_ms:.0f}"
                    unite = "ms"
                avg_time_str = (
                    f'<span style="{common_style}">{valeur}</span>'
                    f'<span style="{common_style} margin-left:4px;">{unite}</span>'
                )
                self.avg_time_label.setText(avg_time_str)
            else:
                self.avg_time_label.setText("N/A")




    def update_table(self, data):
        """
        ================================================================================
        Update table rows from loaded data.
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

    def _clear_layout(self, layout):
        """
        ================================================================================
        Recursively clear all widgets and layouts from a layout.
        ================================================================================
        """
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    @staticmethod
    def time_to_seconds(time_str):
        """
        ================================================================================
        Convert time string (hh:mm:ss or mm:ss) to seconds.
        ================================================================================
        """
        parts = time_str.split(':')
        if len(parts) == 2:  # mm:ss
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:  # hh:mm:ss
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0

    @staticmethod
    def _safe_float(value):
        """
        ================================================================================
        Safe float conversion.
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
        Safe division.
        ================================================================================
        """
        try:
            return round(num / denom, 2) if denom else 0.0
        except Exception:
            return 0.0
