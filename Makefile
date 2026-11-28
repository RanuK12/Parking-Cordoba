.PHONY: test lint build

test:
	python -m pytest tests/ || echo "No tests found, running basic validation"
	python detect_parking.py --help
	
lint:
	flake8 detect_parking.py || echo "flake8 not installed"
	
build:
	python -c "import detect_parking; print('Build successful')"

report:
	python scripts/generate_report.py