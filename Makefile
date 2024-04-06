run:
	uvicorn src.main:app --reload

docker_run:
	cd docker/ && docker compose up --build
