.PHONY: run
run:
	export PROFILE=local && export PYTHONPATH=./running_app && poetry run uvicorn running_app.main:app --host 0.0.0.0 --port 8080
