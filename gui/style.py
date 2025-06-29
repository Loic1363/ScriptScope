# style.py

def apply_mainwindow_style(window):
    window.setStyleSheet("""
        QMainWindow {
            background-color: #111418;
            font-family: 'Inter', 'Noto Sans', sans-serif;
        }
    """)

def apply_table_style(table):
    table.setStyleSheet("""
        QTableWidget {
            background-color: #111418;
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
            background-color: #111418;
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
            background-color: #283039;
            min-height: 2px;
            max-height: 2px;
            border: none;
        }
    """)

def style_title(label):
    label.setStyleSheet("""
        color: #fff;
        font-size: 22px;
        font-family: 'Inter', 'Noto Sans', sans-serif;
        font-weight: bold;
        padding-left: 8px;
        padding-top: 2px;
    """)
