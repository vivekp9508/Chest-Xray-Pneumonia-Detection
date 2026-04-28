import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import cv2

MODEL_PATH = "resnet_pneumonia_finetuned.keras"
model = load_model(MODEL_PATH)
IMG_SIZE = (224, 224)

last_conv_layer_name = "conv5_block3_out"


def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize(IMG_SIZE)
    original = np.array(image)
    arr = img_to_array(image) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr, original


def make_gradcam_heatmap(img_array, original_img):
    grad_model = tf.keras.models.Model(
        inputs=model.input,
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[0][0]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)

    heatmap = np.maximum(heatmap, 0)
    max_val = np.max(heatmap)
    if max_val != 0:
        heatmap /= max_val

    heatmap = cv2.resize(heatmap, IMG_SIZE)
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)

    return overlay


def predict_pneumonia(image):
    img_array, original_img = preprocess_image(image)
    pred = model.predict(img_array)[0][0]

    if pred >= 0.5:
        label = "Pneumonia"
        confidence = pred * 100
    else:
        label = "Normal"
        confidence = (1 - pred) * 100

    heatmap = make_gradcam_heatmap(img_array, original_img)
    return label, confidence, heatmap