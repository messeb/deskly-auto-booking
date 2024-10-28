.PHONY: install run

install:
	@echo "Installing..."
	@pip install -r requirements.txt
	@echo "Done."

run:
	@echo "Book seat..."
	@python3 seatbooking.py
	@echo "Done."
