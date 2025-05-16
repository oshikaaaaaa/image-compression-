from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
from io import BytesIO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def k_means_clustering(image_array: np.ndarray, num_clusters: int, max_iters: int = 10):
    pixels = image_array.reshape(-1, 3).astype(np.float32) / 255.0

    # Initialize cluster centers randomly
    rng = np.random.default_rng()
    indices = rng.choice(pixels.shape[0], size=num_clusters, replace=False)
    cluster_centers = pixels[indices]

    for _ in range(max_iters):
        # Compute distances and assign clusters
        distances = np.linalg.norm(pixels[:, None, :] - cluster_centers[None, :, :], axis=2)
        cluster_assignments = np.argmin(distances, axis=1)

        # Update centers
        new_centers = np.array([
            pixels[cluster_assignments == i].mean(axis=0) if np.any(cluster_assignments == i)
            else cluster_centers[i]
            for i in range(num_clusters)
        ])

        if np.allclose(new_centers, cluster_centers, atol=1e-4):
            break

        cluster_centers = new_centers

    return cluster_assignments, cluster_centers

def compress_image(image_data: bytes, num_clusters: int, max_iters: int = 100) -> BytesIO:
    image = Image.open(BytesIO(image_data)).convert('RGB')
    image_array = np.array(image)

    cluster_assignments, cluster_centers = k_means_clustering(image_array, num_clusters, max_iters)

    # Reconstruct image from clusters
    compressed_pixels = cluster_centers[cluster_assignments]
    compressed_pixels = (compressed_pixels * 255).astype(np.uint8)
    compressed_image = compressed_pixels.reshape(image_array.shape)

    compressed_pil_image = Image.fromarray(compressed_image)

    img_io = BytesIO()
    compressed_pil_image.save(img_io, format='PNG')
    img_io.seek(0)

    return img_io

@app.post("/compress")
async def compress_endpoint(
    image: UploadFile = File(...),
    num_colors: int = Form(2),
    max_iters: int = Form(100)
):
    try:
        if not image.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise HTTPException(status_code=400, detail="Invalid image format. Use .jpg, .jpeg, or .png")

        image_data = await image.read()

        print("Starting compression...")
        img_io = compress_image(image_data, num_clusters=num_colors, max_iters=max_iters)

        return StreamingResponse(img_io, media_type="image/png")

    except Exception as e:
        print(f"Error during compression: {e}")
        return JSONResponse(status_code=500, content={"error": "Image compression failed."})
