# ScriptScope – in development

⚠️ **This project is currently under active development. Features and interfaces may change. Use with caution!**

**ScriptScope** is a professional, modular monitoring tool for Linux environments. It lets you track, visualize, and analyze the resource consumption (CPU, RAM, I/O, and more) of specific scripts within your projects. Unlike generic system monitors, ScriptScope focuses on user-defined scripts, providing targeted insights to help you optimize and manage your automated workflows.

---

## Features

- **Project-based monitoring**: Track only the scripts you care about, not the whole system.
- **Real-time resource usage**: Visualize per-script CPU, memory, I/O, and runtime statistics in real time.
- **Customizable interface**: Modern desktop GUI (PyQt) with color-coded metrics; terminal UI also available.
- **Modular architecture**: Easily extend or replace components (monitoring, UI, configuration, notifications).
- **Notifications and alerts**: Get notified when a script exceeds resource thresholds (CPU, memory, etc.).
- **Automatic recovery**: Optionally restart failed or crashed scripts automatically.
- **Export & reporting**: Save usage reports in CSV or JSON formats for further analysis.
- **Easy integration**: Simple configuration file to declare which scripts to monitor.
- **Lightweight & dependency-minimal**: Runs on any standard Linux distribution with Python and Bash.

---

## Getting Started

### Prerequisites

- Linux (tested on Ubuntu, Debian, Arch)
- Bash (or compatible shell)
- Python 3.7+ (for the GUI)
- Standard Unix tools: `ps`, `awk`, `grep`, `sed`
- Optional for advanced UI: `dialog`, `whiptail`, or `fzf`

### Installation

1. **Clone this repository**  
