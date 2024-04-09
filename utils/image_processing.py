import io
import torch
import torchvision.transforms as transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from PIL import Image

# loads the pre-trained object detection model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()


def detect_cellphone_in_image(image_bytes: bytes)->bool:
    """
    Detects if a cellphone is present in the given image.

    Args:
        image_bytes (bytes): The image data in bytes.

    Returns:
        bool: True if a cellphone is detected, False otherwise.
    """


    # Define transform to preprocess the image
    transform = transforms.Compose([transforms.ToTensor()])
    
    # Process the image
    image = Image.open(io.BytesIO(image_bytes))
    image_tensor = transform(image).unsqueeze(0)
    
    # Perform object detection
    with torch.no_grad():
        prediction = model(image_tensor)
        
    # Check if cellphone is detected
    labels = prediction[0]['labels'].tolist()
    if 77 in labels:  # 77 is the label for cellphone in COCO dataset
        return True
    else:
        return False