.PHONY: start stop build-frontend

INTERFACE ?= eth0
IP_ADDR := $(shell ip -4 addr show $(INTERFACE) | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
PORT := 8000

build-frontend:
	docker-compose build --build-arg VITE_API_BASE_URL="http://$(IP_ADDR):$(PORT)" frontend

start:
	make build-frontend && \
	cd backend && \
	screen -dmS backend bash -c '. ./venv/bin/activate && exec uvicorn main:app --host 0.0.0.0 --port $(PORT) > ../uvicorn.log 2>&1' && \
	docker-compose up -d

stop:
	@if screen -list | grep -q "backend"; then \
		screen -S backend -X quit; \
		echo "Stopped screen session 'backend'."; \
	else \
		echo "No screen session named 'backend' found."; \
	fi

	docker-compose down
