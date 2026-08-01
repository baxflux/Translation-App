from pathlib import Path
import zipfile
import shutil
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

from app.utils.prompt import build_prompt
from app.utils.text_preprocess import preprocess_input
from app.utils.chunking import split_into_sentences, build_chunks

CURRENT_FILE = Path(__file__).resolve()

APP_DIR = CURRENT_FILE.parents[1]
BACKEND_DIR = CURRENT_FILE.parents[2]
PROJECT_ROOT = CURRENT_FILE.parents[3]

MODEL_ROOT = PROJECT_ROOT / "model"
MODEL_ZIP_PATH = MODEL_ROOT / "qwen2.5-0.5b-lora-model.zip"
MODEL_DIR = MODEL_ROOT / "qwen2.5-0.5b-lora-model"

BASE_MODEL = "Qwen/Qwen2.5-0.5B"
DEFAULT_MAX_INPUT_TOKENS = 512
MAX_NEW_TOKENS = 256

# Global variables for model and tokenizer
tokenizer = None
base_model = None
model = None
model_loaded = False

def ensure_model_ready():
    """Prepare model files from zip"""
    if MODEL_DIR.exists():
        print(">>> Removing extracted model directory...")
        shutil.rmtree(MODEL_DIR)

    if not MODEL_ZIP_PATH.exists():
        raise FileNotFoundError(
            f"Model zip not found: {MODEL_ZIP_PATH}"
        )

    print(">>> Extracting LoRA model from zip...")
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(MODEL_ZIP_PATH, "r") as z:
        z.extractall(MODEL_DIR)

    inner_dirs = list(MODEL_DIR.iterdir())
    if len(inner_dirs) == 1 and inner_dirs[0].is_dir():
        for f in inner_dirs[0].iterdir():
            f.rename(MODEL_DIR / f.name)
        inner_dirs[0].rmdir()

    print(">>> Model ready.")

def load_model():
    """Load model and tokenizer (lazy loading - called after server starts)"""
    global tokenizer, base_model, model, model_loaded
    
    if model_loaded:
        return
    
    print("\n>>> Loading Qwen2.5 base model and LoRA adapter...")
    ensure_model_ready()
    
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token

    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        dtype=torch.float32,
        device_map="cpu",
        trust_remote_code=True
    )

    model = PeftModel.from_pretrained(
        base_model,
        MODEL_DIR
    )
    model.eval()
    
    model_loaded = True
    print(">>> Model loaded successfully!\n")

def _translate_chunk(text: str) -> str:
    prompt = build_prompt(text)
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            num_beams=1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded.split("Vietnamese:")[-1].strip()

def translate_long_text(text: str, max_tokens: int = DEFAULT_MAX_INPUT_TOKENS) -> tuple:
    """Translate text and return (translation, duration_in_seconds)"""
    # Ensure model is loaded
    if not model_loaded:
        load_model()
    
    start_time = time.time()
    
    text = preprocess_input(text)

    sentences = split_into_sentences(text)
    if not sentences:
        duration = time.time() - start_time
        return "", round(duration, 2)

    chunks = build_chunks(
        sentences=sentences,
        tokenizer=tokenizer,
        max_tokens=max_tokens
    )

    translations = []
    for chunk in chunks:
        vi = _translate_chunk(chunk)
        translations.append(vi)

    duration = time.time() - start_time
    return "\n".join(translations), round(duration, 2)
