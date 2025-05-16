from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image

client = TestClient(app)

def create_dummy_image():
    img = Image.new("RGB", (50, 50), color=(255, 0, 0))  # Red square
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def test_compress_endpoint():
    img_data = create_dummy_image()

    response = client.post(
        "/compress",
        files={"image": ("test.png", img_data, "image/png")},
        data={"num_colors": 3, "max_iters": 10},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
