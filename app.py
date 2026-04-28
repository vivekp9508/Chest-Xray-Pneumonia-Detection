import gradio as gr
from utils import predict_pneumonia


def analyze_xray(image):
    label, confidence, heatmap = predict_pneumonia(image)

    status_color = "#ef4444" if label == "Pneumonia" else "#22c55e"
    status_icon = "⚠️" if label == "Pneumonia" else "✅"

    result_html = f"""
    <div style='background:white; padding:30px; border-radius:20px;
                box-shadow:0 10px 25px rgba(0,0,0,0.08); text-align:center; margin-top:30px;'>
        <h2 style='color:#1f2937;'>🩺 AI Medical Diagnosis Report</h2>
        <p style='font-size:30px; color:{status_color}; margin:15px;'><b>{status_icon} {label}</b></p>
        <p style='font-size:22px; color:#374151;'><b>Confidence Score:</b> {confidence:.2f}%</p>
    </div>
    """
    return result_html, heatmap


custom_css = """
body {
    background: linear-gradient(135deg, #e0f2fe, #f8fafc);
}
.gradio-container {
    max-width: 1320px !important;
    margin: auto;
}
h1, h2, h3, p {
    text-align: center;
}
footer {
    visibility: hidden;
}
#hero {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft(primary_hue="blue")) as demo:

    gr.HTML("""
    <div id='hero'>
        <h1>🩻 Chest X-Ray Pneumonia Detection AI</h1>
        <h3>Deep Learning Powered Intelligent Medical Image Analysis</h3>
        <p>Upload a chest X-ray scan and receive automated Pneumonia detection with Grad-CAM visual explainability using a fine-tuned ResNet50 model.</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            input_img = gr.Image(type="pil", label="📤 Upload Chest X-Ray Scan", height=430)

        with gr.Column(scale=1):
            output_heatmap = gr.Image(label="🔥 Grad-CAM Heatmap", height=430)

    output_text = gr.HTML()

    analyze_btn = gr.Button("🔍 Analyze Chest X-Ray", size="lg", variant="primary")

    analyze_btn.click(
        fn=analyze_xray,
        inputs=input_img,
        outputs=[output_text, output_heatmap],
        show_progress=True
    )

    gr.Examples(
        examples=[
            ["sample1.jpeg"],
            ["sample2.jpeg"]
        ],
        inputs=input_img,
        label="📁 Test with Sample X-Ray Images"
    )

    gr.HTML("""
    <div style='background:white; margin-top:25px; padding:20px; border-radius:20px;
                box-shadow:0 8px 20px rgba(0,0,0,0.08);'>
        <h2>🚀 Key Features</h2>
        <p>✅ Deep Learning Pneumonia Detection</p>
        <p>✅ Confidence Score Estimation</p>
        <p>✅ Grad-CAM Explainable Visualization</p>
        <p>✅ Browser Based Real-Time Analysis</p>
        <p>✅ Fine-Tuned ResNet50 Transfer Learning</p>
    </div>
    """)

    gr.HTML("""
    <div style='text-align:center; margin-top:25px; color:#374151;'>
        <h3>👨‍💻 Developed by Vivek Pandey</h3>
        <p>GitHub: https://github.com/vivekp9508/chest-xray-pneumonia-detection</p>
    </div>
    """)

demo.launch()
