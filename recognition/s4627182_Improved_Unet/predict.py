import torch
from torchvision import transforms
from PIL import Image
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def segment_image(model_path, image_path, output_path):

    # Load the pre-trained model
    model = torch.load(model_path)
    model.to(device)
    model.eval()

    # Load and preprocess the image
    img = Image.open(image_path)  # Adjust the size as per your model's requirements
    img_np = np.array(img) / 255.0
    img_tensor = torch.tensor(img_np).to(device)

    # Predict the mask
    with torch.no_grad():
        predicted_mask = model(img_tensor)

    # Convert mask to numpy array
    predicted_mask = predicted_mask.squeeze().cpu().numpy()
    predicted_mask_image = (predicted_mask * 255).astype(np.uint8)

    predicted_mask_image.save(output_path)

    return predicted_mask_image

# Example usage:
# segmented_img = segment_image("path_to_model.pth", "path_to_image.jpg")
# Image.fromarray(segmented_img).save("segmented_output.png")
