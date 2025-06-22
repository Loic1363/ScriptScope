.PHONY: start clean

START_CMD = bin/scriptscope.sh ui
PID_FILE = .scriptscope.pid

start:
	@echo "Starting ScriptScope UI..."
	@nohup $(START_CMD) > scriptscope.log 2>&1 & echo $$! > $(PID_FILE)
	@echo "ScriptScope started with PID $$(cat $(PID_FILE))"

clean:
	@if [ -f $(PID_FILE) ]; then \
		PID=$$(cat $(PID_FILE)); \
		echo "Stopping ScriptScope (PID $$PID)..."; \
		kill $$PID && rm -f $(PID_FILE); \
		echo "ScriptScope stopped."; \
	else \
		echo "No ScriptScope process found."; \
	fi
