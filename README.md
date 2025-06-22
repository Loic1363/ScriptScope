# ScriptScope

ScriptScope is a professional, modular monitoring tool designed for Linux environments. It enables you to track, visualize, and analyze the resource consumption (CPU, RAM, etc.) of specific scripts within your projects. Unlike generic system monitors, ScriptScope focuses on user-defined scripts, providing targeted insights to help you optimize and manage your automated workflows.

## Features

- **Project-based monitoring:** Track only the scripts you care about.
- **Real-time resource usage:** Visualize CPU, memory, and runtime stats per script.
- **Customizable interface:** Clean, interactive terminal UI (with optional web dashboard in the future).
- **Modular architecture:** Easily extend or replace components (monitoring, UI, config, notifications).
- **Notifications and alerts:** Get notified when a script exceeds resource thresholds.
- **Automatic recovery:** Optionally restart failed scripts.
- **Export & reporting:** Save usage reports in CSV or JSON formats.

## Getting Started

### Prerequisites

- Linux (tested on Ubuntu, Debian, Fedora)
- Bash (or compatible shell)
- `ps`, `top`, `awk`, `grep`, `sed`, `tmux` or `screen` (for advanced UI)
- Optional: `dialog`, `whiptail`, or `fzf` for enhanced UI

### Installation

