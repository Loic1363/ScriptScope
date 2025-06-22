import sys
from PyQt5.QtWidgets import QApplication
from gui.widgets import ScriptScopeMainWindow

def main():
    app = QApplication(sys.argv)
    window = ScriptScopeMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
