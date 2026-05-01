import gradio as gr
from utils import predict_pneumonia

def analyze_xray(image):
    if image is None:
        return """
        <div class="empty-report">
            <div class="empty-icon">🩺</div>
            <div class="empty-title">Awaiting X-Ray Analysis</div>
            <div class="empty-sub">Upload a chest X-ray image and click analyze to generate AI diagnostic insights.</div>
        </div>
        """, None

    label, confidence, heatmap = predict_pneumonia(image)

    if label == "Pneumonia":
        accent = "#ef4444"
        soft_accent = "rgba(239,68,68,0.14)"
        border = "rgba(239,68,68,0.35)"
        badge = "HIGH RISK DETECTED"
        icon = "⚠"
        bar = "linear-gradient(90deg,#ef4444,#f87171)"
    else:
        accent = "#10b981"
        soft_accent = "rgba(16,185,129,0.14)"
        border = "rgba(16,185,129,0.35)"
        badge = "NO PATHOLOGY FOUND"
        icon = "✓"
        bar = "linear-gradient(90deg,#10b981,#34d399)"

    result_html = f"""
    <div class="report-card" style="border:1px solid {border}; box-shadow:0 0 35px {soft_accent};">
        <div class="report-header">
            <div class="report-left">
                <div class="live-dot" style="background:{accent};"></div>
                <div>
                    <div class="report-mini">AI DIAGNOSTIC REPORT</div>
                    <div class="report-sub">ResNet50 • Grad-CAM • Confidence Mapping</div>
                </div>
            </div>
            <div class="report-badge" style="background:{soft_accent}; color:{accent}; border:1px solid {border};">{badge}</div>
        </div>

        <div class="report-body">
            <div class="diag-label">Primary Diagnosis</div>
            <div class="diag-value"><span style="color:{accent};">{icon}</span> {label}</div>

            <div class="divider-line"></div>

            <div class="conf-row">
                <span>Model Confidence</span>
                <span style="color:{accent};">{confidence:.1f}%</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" style="width:{int(confidence)}%; background:{bar};"></div>
            </div>

            <div class="heatmap-note">
                🔍 Grad-CAM highlights medically influential lung regions used in model decision.
            </div>

            <div class="medical-note">
                ⚕ For academic demonstration only. This AI output should not be treated as a substitute for certified radiological diagnosis.
            </div>
        </div>
    </div>
    """
    return result_html, heatmap

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*{box-sizing:border-box;font-family:'Inter',sans-serif !important;}

body, .gradio-container, .main, .wrap{
background: 
radial-gradient(circle at top center, rgba(124,58,237,0.08), transparent 28%),
radial-gradient(circle at 20% 30%, rgba(99,102,241,0.05), transparent 25%),
#06070b !important;
}

.gradio-container{max-width:1180px !important;margin:auto !important;padding:0 24px 70px !important;}
p, span, label, div{color:#cbd5e1;}

.navbar{
background:rgba(13,19,32,0.75);
backdrop-filter:blur(12px);
border:1px solid rgba(148,163,184,0.08);
border-radius:18px;
padding:16px 24px;
margin-top:18px;
margin-bottom:55px;
display:flex;justify-content:space-between;align-items:center;
box-shadow:0 10px 40px rgba(0,0,0,0.25);
}

.glass-card{
background:linear-gradient(180deg, rgba(13,19,32,0.95), rgba(9,12,20,0.95));
border:1px solid rgba(148,163,184,0.12);
border-radius:18px;padding:22px;transition:all .35s ease;
box-shadow:0 8px 30px rgba(0,0,0,0.22);
}
.glass-card:hover{transform:translateY(-5px);border-color:rgba(124,58,237,0.28);box-shadow:0 12px 35px rgba(124,58,237,0.12);}

/* --- IMAGE SCALING FIX --- */
.upload-box, .heatmap-box { width: 100% !important; }

.upload-box .wrap, .heatmap-box .wrap {
background:#0d1320 !important;
border:1.5px solid rgba(148,163,184,0.12) !important;
border-radius:18px !important;
min-height:360px !important;
width: 100% !important;
display: flex !important;
flex-direction: column !important;
overflow: hidden !important;
justify-content: center !important;
align-items: center !important;
}

/* This targets the actual image to make it fit the box */
.upload-box img, .heatmap-box img {
    width: 100% !important;
    height: 100% !important;
    object-fit: contain !important; /* Ensures the whole image is visible and as large as possible */
}

.upload-box .wrap {
border:1.5px dashed rgba(124,58,237,0.35) !important;
}

.upload-box .footer, .heatmap-box .footer {
display: none !important; /* Keeps the grey icon bar hidden */
}

.upload-box button, .upload-box .upload-container {
width: 100% !important;
flex: 1 !important;
background: transparent !important;
display: flex !important;
flex-direction: column !important;
justify-content: center !important;
align-items: center !important;
}

.upload-box .wrap:hover{border-color:rgba(124,58,237,0.8) !important;box-shadow:0 0 20px rgba(124,58,237,0.08) inset;}

#analyze-btn{
width:100% !important;margin-top:16px !important;border:none !important;border-radius:14px !important;padding:16px !important;
font-size:15px !important;font-weight:700 !important;color:white !important;
background:linear-gradient(135deg,#7c3aed,#6366f1) !important;
box-shadow:0 10px 30px rgba(99,102,241,0.28) !important;transition:all .3s ease !important;
cursor: pointer;
}
#analyze-btn:hover{transform:translateY(-3px);box-shadow:0 16px 38px rgba(99,102,241,0.38) !important;}

/* --- REPORT STYLES --- */
.report-card{background:#0d1320;border-radius:18px;margin-top:16px;overflow:hidden;}
.report-header{padding:18px 22px;border-bottom:1px solid rgba(148,163,184,0.08);display:flex;justify-content:space-between;align-items:center;}
.report-left{display:flex;gap:10px;align-items:center;}
.live-dot{width:10px;height:10px;border-radius:50%;animation:pulse 1.8s infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(255,255,255,0.4);}100%{box-shadow:0 0 0 10px rgba(255,255,255,0);}}
.report-mini{font-size:11px;font-weight:700;letter-spacing:1.6px;color:#f8fafc;}
.report-sub{font-size:12px;color:#94a3b8;}
.report-badge{font-size:10px;font-weight:700;padding:6px 12px;border-radius:999px;}
.report-body{padding:22px;}
.diag-label{font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:1.3px;margin-bottom:8px;}
.diag-value{font-size:30px;color:#f8fafc;font-weight:800;}
.divider-line{height:1px;background:rgba(148,163,184,0.08);margin:20px 0;}
.conf-row{display:flex;justify-content:space-between;margin-bottom:8px;font-weight:600;}
.progress-track{width:100%;height:8px;background:rgba(255,255,255,0.06);border-radius:999px;overflow:hidden;}
.progress-fill{height:100%;border-radius:999px;}
.heatmap-note{margin-top:16px;color:#a5b4fc;font-size:12px;line-height:1.7;}
.medical-note{margin-top:16px;padding:12px;border-radius:12px;background:rgba(255,255,255,0.03);border:1px solid rgba(148,163,184,0.08);font-size:11px;color:#94a3b8;line-height:1.7;}

.empty-report{background:#0d1320;border:1px dashed rgba(148,163,184,0.12);border-radius:18px;margin-top:16px;padding:42px 24px;text-align:center;}
.empty-icon{font-size:34px;margin-bottom:10px;}
.empty-title{font-size:18px;font-weight:700;color:#f8fafc;margin-bottom:8px;}
.empty-sub{font-size:13px;color:#94a3b8;line-height:1.7;}

.tech-pill {
    padding:6px 12px;border-radius:8px;background:#0d1320;
    border:1px solid rgba(148,163,184,0.08);font-size:11px;
}

footer{display:none !important;}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Base(), title="PneumoScan AI") as demo:

    # ── Navbar ──
    gr.HTML("""
    <div class="navbar">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#7c3aed,#6366f1);display:flex;align-items:center;justify-content:center;font-size:18px;">🩻</div>
            <div style="font-size:20px;font-weight:800;color:#f8fafc;">PneumoScan<span style="color:#a78bfa;">AI</span></div>
        </div>
        <div style="font-size:11px;color:#94a3b8;">ResNet50 • Transfer Learning • Explainable AI • Live Demo</div>
    </div>
    """)

    # ── Hero ──
    gr.HTML("""
    <div style="text-align:center;padding:0 20px 55px;">
        <div style="display:inline-block;padding:8px 18px;border-radius:999px;background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.22);font-size:11px;font-weight:700;color:#c4b5fd;letter-spacing:1px;">
            AI-POWERED • MEDICAL IMAGING • EXPLAINABLE AI
        </div>
        <h1 style="font-size:56px;line-height:1.1;color:#f8fafc;margin:24px 0 16px;font-weight:900;">
            Chest X-Ray <br><span style="background:linear-gradient(135deg,#a78bfa,#6366f1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Pneumonia Detection</span>
        </h1>
        <p style="max-width:700px;margin:auto;font-size:15px;color:#94a3b8;line-height:1.9;">
            Upload a chest X-ray image and receive an instant AI-generated pneumonia assessment powered by a fine-tuned ResNet50 model with Grad-CAM visual explainability.
        </p>
    </div>
    """)

    # ── Stat Cards ──
    gr.HTML("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:42px;">
        <div class="glass-card"><div style="font-size:11px;color:#94a3b8;">ARCHITECTURE</div><div style="font-size:24px;font-weight:800;color:#f8fafc;margin:8px 0;">ResNet50</div><div style="font-size:13px;color:#94a3b8;">Fine-tuned CNN trained on chest radiography dataset</div></div>
        <div class="glass-card"><div style="font-size:11px;color:#94a3b8;">EXPLAINABILITY</div><div style="font-size:24px;font-weight:800;color:#f8fafc;margin:8px 0;">Grad-CAM</div><div style="font-size:13px;color:#94a3b8;">Heatmap localization of disease-influencing regions</div></div>
        <div class="glass-card"><div style="font-size:11px;color:#94a3b8;">INPUT SIZE</div><div style="font-size:24px;font-weight:800;color:#f8fafc;margin:8px 0;">224 × 224</div><div style="font-size:13px;color:#94a3b8;">ImageNet normalized medical image preprocessing</div></div>
    </div>
    """)

    # ── Main Content ──
    with gr.Row():
        with gr.Column():
            gr.HTML("<div style='margin-bottom:10px;font-size:12px;color:#94a3b8;font-weight:700;'>01 — Upload Chest X-Ray</div>")
            input_img = gr.Image(type="pil", label="", height=360, elem_classes=["upload-box"])
            gr.Examples(
                examples=[["sample1.jpeg"], ["sample2.jpeg"], ["sample3.jpeg"], ["sample4.jpeg"], ["sample5.jpeg"]],
                inputs=input_img,
                label="📁 Try sample X-ray images"
            )
            analyze_btn = gr.Button("⟳ Analyze X-Ray", elem_id="analyze-btn")

        with gr.Column():
            gr.HTML("<div style='margin-bottom:10px;font-size:12px;color:#94a3b8;font-weight:700;'>02 — Grad-CAM Heatmap + Report</div>")
            output_heatmap = gr.Image(label="", height=360, elem_classes=["heatmap-box"])
            output_text = gr.HTML("""
            <div class="empty-report">
                <div class="empty-icon">🧠</div>
                <div class="empty-title">AI Diagnostic Panel Ready</div>
                <div class="empty-sub">Heatmap visualization and diagnostic report will appear here after analysis.</div>
            </div>
            """)

    # ── How It Works ──
    gr.HTML("""
    <div style="margin-top:70px;margin-bottom:48px;">
        <div style="text-align:center;font-size:13px;color:#c4b5fd;font-weight:700;letter-spacing:1px;margin-bottom:24px;">HOW THE SYSTEM WORKS</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
            <div class="glass-card"><div style="font-size:28px;">📤</div><div style="font-size:15px;font-weight:700;color:#f8fafc;margin:12px 0 6px;">Upload Image</div><div style="font-size:12px;color:#94a3b8;">Provide chest X-ray scan in PNG/JPEG format.</div></div>
            <div class="glass-card"><div style="font-size:28px;">⚙</div><div style="font-size:15px;font-weight:700;color:#f8fafc;margin:12px 0 6px;">Preprocess</div><div style="font-size:12px;color:#94a3b8;">Resize, normalize and prepare image tensor.</div></div>
            <div class="glass-card"><div style="font-size:28px;">🧠</div><div style="font-size:15px;font-weight:700;color:#f8fafc;margin:12px 0 6px;">Inference</div><div style="font-size:12px;color:#94a3b8;">ResNet50 predicts Normal or Pneumonia.</div></div>
            <div class="glass-card"><div style="font-size:28px;">🔍</div><div style="font-size:15px;font-weight:700;color:#f8fafc;margin:12px 0 6px;">Explainability</div><div style="font-size:12px;color:#94a3b8;">Grad-CAM shows infected lung areas.</div></div>
        </div>
    </div>
    """)

    # ── Footer ──
    gr.HTML("""
    <div style="margin-top:55px;border-top:1px solid rgba(148,163,184,0.08);padding-top:26px;text-align:center;">
        <div style="margin-bottom:12px;">
            <div style="font-size:14px;font-weight:700;color:#f8fafc;">Built by Vivek Pandey</div>
            <div style="font-size:12px;color:#94a3b8;">
                AI Powered Pneumonia Detection using Deep Learning and Explainable Medical Imaging
            </div>
        </div>
        <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap;">
            <span class="tech-pill">Python</span>
            <span class="tech-pill">TensorFlow</span>
            <span class="tech-pill">Keras</span>
            <span class="tech-pill">Grad-CAM</span>
            <span class="tech-pill">OpenCV</span>
            <span class="tech-pill">NumPy</span>
        </div>
    </div>
    """)

    analyze_btn.click(
        fn=analyze_xray,
        inputs=input_img,
        outputs=[output_text, output_heatmap],
        show_progress=True
    )

demo.launch()