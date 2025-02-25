import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Define paths
dataset_path = "dataset"
stroke_path = os.path.join(dataset_path, "Stroke")
normal_path = os.path.join(dataset_path, "Normal")

# Image enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
def enhance_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)  # Convert to LAB color space
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l_enhanced = clahe.apply(l)
    
    lab = cv2.merge((l_enhanced, a, b))
    enhanced_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    return enhanced_img

# Data preprocessing function
def load_and_preprocess_images(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (224, 224))  # Resize for VGG16
            img = enhance_image(img)  # Apply enhancement
            images.append(img)
            labels.append(label)
    return np.array(images), np.array(labels)

# Load dataset
stroke_images, stroke_labels = load_and_preprocess_images(stroke_path, 1)
normal_images, normal_labels = load_and_preprocess_images(normal_path, 0)

# Combine data
X = np.vstack((stroke_images, normal_images))
y = np.hstack((stroke_labels, normal_labels))

# Normalize images
X = X / 255.0  # Scale pixel values

# Split dataset
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Data Augmentation
datagen = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2, 
                             horizontal_flip=True, zoom_range=0.2, brightness_range=[0.8, 1.2])

# Load VGG16 model (Pretrained on ImageNet)
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
for layer in base_model.layers:
    layer.trainable = False  # Freeze base model layers

# Custom model on top of VGG16
model = Sequential([
    base_model,
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Binary classification
])

# Compile model
model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

# Train model
model.fit(datagen.flow(X_train, y_train, batch_size=32), validation_data=(X_val, y_val), epochs=10)

# Save the trained model
model.save("brain_stroke_vgg16.h5")

print("Model training completed and saved as 'brain_stroke_vgg16.h5'")
