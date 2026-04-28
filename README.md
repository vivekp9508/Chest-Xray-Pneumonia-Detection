
# Chest X-Ray Pneumonia Detection using Deep Learning

A deep learning-based medical image classification web application that detects Pneumonia from Chest X-Ray scans using a fine-tuned ResNet50 model with Grad-CAM explainability.

---

## Features

- Upload Chest X-Ray image
- Predict Normal or Pneumonia
- Display Confidence Score
- Generate Grad-CAM Heatmap
- Interactive Web App using Gradio

---

## Tech Stack

- Python
- TensorFlow / Keras
- ResNet50
- OpenCV
- NumPy
- Gradio

---

## Project Structure 
```bash
Chest-Xray-Pneumonia-Detection/
│
├── .gitignore
├── README.md
├── app.py
├── requirements.txt
└── utils.py
```

---

## How It Works

* Preprocess uploaded Chest X-Ray image
* Perform prediction using trained ResNet50 model
* Classify image as Normal or Pneumonia
* Calculate confidence score
* Generate Grad-CAM explainability heatmap
* Display result on Gradio interface

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/vivekp9508/Chest-Xray-Pneumonia-Detection.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
python app.py
```

---

## Sample Output

* Chest X-Ray Upload Interface
  <img width="1919" height="1025" alt="image" src="https://github.com/user-attachments/assets/f2c6912d-1ef9-46fb-b565-13acb8becdc9" />

* Prediction Result with Confidence
  <img width="1919" height="1024" alt="image" src="https://github.com/user-attachments/assets/b54d848d-c394-440c-a185-6ec0698514cb" />

* Grad-CAM Heatmap Visualization
<img width="598" height="276" alt="image" src="https://github.com/user-attachments/assets/3985ca59-b053-490e-b62b-1ae02a228639" />


---

## Future Scope

* Multi-disease Chest X-Ray detection
* Cloud deployment
* PDF report generation
* Medical dashboard integration

---

```
