import cv2
import numpy as np
import tensorflow as tf

# Load the trained model
model = tf.keras.models.load_model("brain_stroke_vgg16.h5")

# Image preprocessing function (same as used during training)
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None  # Handle error if image is not found

    img = cv2.resize(img, (224, 224))  # Resize to match model input size

    # Apply CLAHE for image enhancement
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l_enhanced = clahe.apply(l)
    lab = cv2.merge((l_enhanced, a, b))
    enhanced_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Normalize pixel values
    enhanced_img = enhanced_img / 255.0  
    enhanced_img = np.expand_dims(enhanced_img, axis=0)  # Add batch dimension

    return enhanced_img

# Analyze image function using trained model
def analyze_image(image_path):
    processed_img = preprocess_image(image_path)
    if processed_img is None:
        return ("Error: Image not found or cannot be processed.", None)  # Always return two values

    prediction = model.predict(processed_img)[0][0]  # Extract single value
    confidence = round(prediction * 100, 2)  

    if prediction > 0.5:
        result = "Stroke Detected"
        summary = f"The model predicts a stroke with {confidence}% confidence. Consult a neurologist."
    else:
        result = "No Stroke Detected"
        confidence = round((1 - prediction) * 100, 2)
        summary = f"The model does not detect a stroke with {confidence}% confidence."

    return (result, summary)  # Ensure it's always a tuple
