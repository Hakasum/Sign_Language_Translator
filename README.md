# project_root/README.md

# Sign Language Detection with YOLOv8

A real-time sign language detector using a YOLOv8 model and OpenCV. Signs are tracked and translated into text using holding durations and gesture detection logic.

---

## Project Structure

```
project_root/
├── README.md
├── requirements.txt
├── config.yaml
├── .gitignore
├── models/
│   └── best.pt               # Your YOLOv8 model (or a placeholder)
├── data/
│   └── sample_images/
│       └── test_image.jpg    # Test image for the notebook
├── notebooks/
│   └── sign_language_detector_testing.ipynb  # Jupyter notebook for testing
└── src/
    ├── main.py               # Main real-time detection script
    ├── detection.py          # Model loading and inference logic
    └── utils.py              # Helper functions (e.g., filtering detections)

```

---

## Getting Started

### 1. Clone the repository
```bash
# Replace with your actual GitHub repository URL
# TODO: Update with your GitHub repo link
git clone https://github.com/Hakasum/Sign_Language_Translator.git
cd Sign_Language_Translator
```

### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare your YOLOv8 model
Place your trained YOLOv8 model in the `models/` directory and name it `best.pt` (or update `config.yaml` to match your filename).

---

## Configuration
Edit `config.yaml` to change thresholds, model path, and gesture keywords:

```yaml
model_path: "models/V5-3-3.pt"
space_sign: "Space"
delete_sign: "Delete"
confidence_threshold: 0.9
default_hold_time: 0.7
functional_hold_time: 1.0
cooldown_time: 5.0
max_detections: 1
```

---

## How It Works
- Loads a YOLOv8 model to detect hand signs in webcam frames
- Uses ByteTrack to track objects across frames
- Tracks how long each detection is held to decide whether to add a sign
- Space and delete signs have special behaviors
- Displays the evolving sentence on the screen in real-time

---

## Running the App
```bash
python src/main.py
```
Make sure your webcam is connected and accessible.

