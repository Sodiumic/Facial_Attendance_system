import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "database.db")

DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAINER_DIR = os.path.join(BASE_DIR, "trainer")
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

MODEL_FILE = os.path.join(TRAINER_DIR, "face_model.yml")
LABELS_FILE = os.path.join(TRAINER_DIR, "labels.json")

CAMERA_INDEX = 0
FACE_WIDTH = 200
FACE_HEIGHT = 200
MAX_IMAGES = 50

CONFIDENCE_THRESHOLD = 70

SENDER_EMAIL = ""
SENDER_PASSWORD = ""

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(TRAINER_DIR, exist_ok=True)
os.makedirs(ATTENDANCE_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)