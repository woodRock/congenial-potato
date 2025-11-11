from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Run the model on the image
results = model('../figures/underwater_fish.jpg')

# Save the annotated image
for r in results:
    r.save(filename='../annotated_fish_yolov8.jpg')

print("Annotated image saved as annotated_fish_yolov8.jpg")