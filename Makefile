.PHONY: start ui test-scripts clean

PYTHON = python3
GUI_MAIN = gui/main.py

test-scripts:
	@chmod +x example/*.sh
	@./example/cpu_stress.sh &
	#@sleep 4
	@./example/mem_stress.sh &
	@./example/io_stress.sh &
	#@sleep 3
	@./example/sleep_script.sh &

start: test-scripts
	@echo "Starting ScriptScope in terminal mode..."
	@./modules/ui.sh

ui: clean test-scripts
	@echo "Starting ScriptScope monitor..."
	@(while true; do ./modules/monitor.sh; sleep 1; done) & \
	MONITOR_PID=$$!; \
	echo "Starting ScriptScope GUI..."; \
	python3 -m gui.main; \
	echo "Stopping monitor..."; \
	kill $$MONITOR_PID 2>/dev/null || true

clean:
	-@pgrep -f cpu_stress.sh | xargs -r kill || true
	-@pgrep -f mem_stress.sh | xargs -r kill || true
	-@pgrep -f io_stress.sh | xargs -r kill || true
	-@pgrep -f sleep_script.sh | xargs -r kill || true
