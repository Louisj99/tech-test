.PHONY: run test

run:
	poetry run python -m flask --app user_monitoring.main:app run --debug
	#poetry run flask --app user_monitoring.main:app run --debug <--- i had trouble with running run this command, so i used the above command


test:
	poetry run python -m pytest -vvv
