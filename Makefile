server:
	uvicorn src.main:app --reload

order_processing_app:
	python -m src.run_consumer

docker_up:
	cd docker/ && docker compose up --build

data_docker_up:
	cd docker/ && docker compose up pgdb kafka

test:
	pytest -vv -s
