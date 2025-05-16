
# Image Compressor API

Compress images by reducing colors using K-Means clustering. Built with FastAPI and NumPy.

## Setup

### Clone and enter the repository:

```bash
git clone https://github.com/yourusername/image_compressor.git
cd image_compressor

## Create and activate virtual env:
	python -m venv venv
	source venv/bin/activate  # or .\venv\Scripts\activate on Windows

## Install dependencies:
	  pip install -r requirements.txt
	  
## Run
Start server locally:

	uvicorn app.main:app --reload

Or use Docker:

	docker build -t image_compressor .
	docker run -p 8000:8000 image_compressor

