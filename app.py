import gradio as gr
from utils import predict_pneumonia


def analyze_xray(image):
    label, confidence, heatmap = predict_pneumonia(image)
    result = f"Prediction: {label}\nConfidence: {confidence:.2f}%"
    return result, heatmap


with gr.Blocks() as demo:
    gr.Markdown("# Chest X-Ray Pneumonia Detection using Deep Learning")
    gr.Markdown("Upload a chest X-ray image to classify it as Normal or Pneumonia with Grad-CAM explainability.")

    with gr.Row():
        input_img = gr.Image(type="pil", label="Upload Chest X-Ray")
        output_text = gr.Textbox(label="Prediction Result")
        output_heatmap = gr.Image(label="Grad-CAM Heatmap")

    submit_btn = gr.Button("Analyze Image")
    submit_btn.click(fn=analyze_xray, inputs=input_img, outputs=[output_text, output_heatmap])

demo.launch()