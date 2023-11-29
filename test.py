from ultralytics import YOLO

# تحميل الموديل
model = YOLO('weights/yolov8s-pose.pt')

# مصدر الموديل (فديو \ ويب كام)
results = model(source="https://youtu.be/wJOaKsop9zw?si=gSSGx3Lb5muCvY_b", show=True, conf=0.3, save=True)