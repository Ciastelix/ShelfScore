import os
from uuid import UUID
from PIL import Image


class ImageService:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def save_image(self, user_id: UUID, file) -> str:
        # Define the image path
        image_path = os.path.join(self.upload_dir, f"{user_id}.png")

        # Save the uploaded file
        with open(image_path, "wb") as buffer:
            buffer.write(await file.read())

        # Open the image and convert to PNG if necessary
        with Image.open(image_path) as img:
            if img.format != "PNG":
                img = img.convert("RGB")
                img.save(image_path, "PNG")

        return image_path
