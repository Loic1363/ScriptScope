# style.py
from PyQt5.QtCore import Qt

def style_script_label(label):
    label.setFixedWidth(100)
    label.setAlignment(Qt.AlignLeft)
    label.setStyleSheet("""
        color: #919ead;
        margin: 0;
        padding: 0;
        border: none;
    """)
    label.setToolTip(label.text())

def apply_mainwindow_style(window):
    window.setStyleSheet("""
        QMainWindow {
            background-color: #1b2027;
            font-family: 'Inter', 'Noto Sans', sans-serif;
        }
    """)

def apply_table_style(table):
    table.setStyleSheet("""
        QTableWidget {
            background-color: #1b2027;
            color: #f8f8f2;
            border: 1px solid #3b4754;
            border-radius: 12px;
            font-family: 'Inter', 'Noto Sans', sans-serif;
            font-size: 15px;
            selection-background-color: #283039;
            selection-color: #fff;
            gridline-color: #283039;
        }
        QHeaderView::section {
            background-color: #1b2127;
            color: #fff;
            font-weight: bold;
            font-size: 14px;
            border: none;
            padding: 10px 0 10px 10px;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background-color: #283039;
            color: #fff;
        }
    """)

def style_button(btn):
    btn.setStyleSheet("""
        QPushButton {
            background-color: #1b2027;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 16px 18px;
            font-size: 15px;
            font-family: 'Inter', 'Noto Sans', sans-serif;
            font-weight: 500;
        }
        QPushButton:hover {
            background-color: #3b4754;
            border: none;
        }
        QPushButton:pressed {
            background-color: #22262b;
            border: none;
        }
        QPushButton:focus {
            border: none;
            outline: none;
        }
        QPushButton:checked {
            border: none;
        }
    """)

def style_separator(frame):
    frame.setStyleSheet("""
        QFrame {
            background-color: #394450;
            min-height: 2px;
            max-height: 2px;
            border: none;
        }
    """)

def style_title(label):
    label.setStyleSheet("""
        color: #fff;
        font-size: 24px;
        font-family: 'Inter', 'Noto Sans', sans-serif;
        font-weight: bold;
        padding-left: 8px;
        padding-top: 2px;
    """)

def style_overview_title(label):
    label.setStyleSheet("""
        color: #fff;
        font-size: 26px;
        font-family: 'Inter', 'Noto Sans', sans-serif;
        font-weight: bold;
        margin-top: 32px;
        margin-bottom: 4px;
    """)

def style_overview_subtitle(label):
    label.setStyleSheet("""
        color: #919ead;
        font-size: 15px;
        font-family: 'Inter', 'Noto Sans', sans-serif;
        background: #1b2027;
        border-radius: 8px;
        padding-top: 16px;
        padding-bottom: 16px;
        padding-left: 1px;       
        padding-right: 24px;    
        margin-bottom: 4px;
    """)

def style_metrics_rect(rect):
    rect.setStyleSheet("""
        background: #1b2027;
        border-radius: 12px;
        border: 1px solid #3b4754
    """)

def style_metrics_title(label):
    label.setStyleSheet("""
        color: #fff;
        font-size: 18px;
        font-weight: normal;
        background: none;
        border: none;
        border-radius: 0;
        padding-top: 5px;       
        margin: 0;
    """)

def style_script_label(label):
    label.setFixedWidth(100)  
    label.setAlignment(Qt.AlignLeft) 
    label.setStyleSheet("""
        color: #919ead;
        margin: 0;
        padding: 0;
        border: none;
    """)
    label.setToolTip(label.text())  


def style_script_progress_bar(bar):
    bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid #3b4754;
            border-radius: 4px;
            background: #1b2027;
            height: 12px;
        }
        QProgressBar::chunk {
            background: #919ead;
            border-radius: 4px;
        }
    """)

def style_no_scripts_label(label):
    label.setStyleSheet("""
        color: #919ead;
        border: none;
        margin: 0;
        padding: 0;
    """)

