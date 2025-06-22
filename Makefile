.PHONY: start clean test-scripts

START_CMD = bin/scriptscope.sh ui
PID_FILE = .scriptscope.pid

test-scripts:
	@chmod +x example/*.sh
	@./example/cpu_stress.sh &
	@./example/mem_stress.sh &
	@./example/io_stress.sh &
	@./example/sleep_script.sh &

start: test-scripts
	@echo "Starting ScriptScope UI..."
	@echo "Starting ScriptScope UI (interactive mode)..."
	@$(START_CMD)
	@echo "ScriptScope started with PID $$(cat $(PID_FILE))"

clean:
	@if [ -f $(PID_FILE) ]; then \
		PID=$$(cat $(PID_FILE)); \
		echo "Stopping ScriptScope (PID $$PID)..."; \
		kill $$PID 2>/dev/null || true; \
		rm -f $(PID_FILE); \
		echo "ScriptScope stopped."; \
	else \
		echo "No ScriptScope process found."; \
	fi
	@pkill -f cpu_stress.sh || true
	@pkill -f mem_stress.sh || true
	@pkill -f io_stress.sh || true
	@pkill -f sleep_script.sh || true
