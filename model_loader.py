import os
import zipfile
import shutil
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def unzip_lora(lora_zip_path, target_dir):
    """
    Giải nén file zip LoRA vào thư mục đích (target_dir).
    - Nếu target_dir đã tồn tại: bỏ qua.
    - Giải nén vào thư mục tạm 'model/_tmp_extract'.
    - Nếu zip chứa 1 thư mục gốc (vd. 'checkpoint-2625' hoặc 'qwen2.5-lora-en-vi'),
      sẽ di chuyển nội dung bên trong thư mục đó vào target_dir.
    - Nếu zip chứa các file ở root, sẽ di chuyển trực tiếp các file đó vào target_dir.
    - Sau cùng: dọn thư mục tạm.
    """
    if not os.path.exists(lora_zip_path):
        print("⚠️ No LoRA zip found, skipping unzip.")
        return

    if os.path.exists(target_dir):
        print("ℹ️ LoRA directory already exists — skipping unzip.")
        return

    tmp_dir = os.path.join("model", "_tmp_extract")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.makedirs(tmp_dir, exist_ok=True)

    print(f"📦 Extracting {lora_zip_path} into temporary folder {tmp_dir} ...")
    with zipfile.ZipFile(lora_zip_path, "r") as zip_ref:
        zip_ref.extractall(tmp_dir)

    # After extraction, determine source folder that contains the LoRA files
    # Prefer a folder named exactly as target_dir basename, else if only one subdir exists, use it,
    # else assume files are directly in tmp_dir.
    candidate_src = None
    tmp_entries = os.listdir(tmp_dir)
    # If zip extracted a top-level folder with the same basename as target_dir
    target_basename = os.path.basename(target_dir.rstrip("/\\"))
    if target_basename in tmp_entries:
        candidate_src = os.path.join(tmp_dir, target_basename)
    else:
        # If there's exactly one entry and it's a directory -> probably checkpoint-xxxx
        if len(tmp_entries) == 1 and os.path.isdir(os.path.join(tmp_dir, tmp_entries[0])):
            candidate_src = os.path.join(tmp_dir, tmp_entries[0])
        else:
            # otherwise the files are directly in tmp_dir
            candidate_src = tmp_dir

    # Create target_dir and move contents from candidate_src into it
    os.makedirs(target_dir, exist_ok=True)

    # Move all files/subdirs from candidate_src into target_dir
    for name in os.listdir(candidate_src):
        src_path = os.path.join(candidate_src, name)
        dst_path = os.path.join(target_dir, name)
        # If destination exists, remove it first (to avoid move errors)
        if os.path.exists(dst_path):
            if os.path.isdir(dst_path):
                shutil.rmtree(dst_path)
            else:
                os.remove(dst_path)
        shutil.move(src_path, dst_path)

    # Clean up temporary extraction folder
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    print(f"✅ LoRA zip extracted and moved to: {target_dir}")


def load_model():
    """Load base model và LoRA adapter (nếu có)."""
    base_model_name = "Qwen/Qwen2.5-0.5B"
    lora_zip = "model/qwen2.5-lora.zip"
    lora_dir = "model/qwen2.5-lora-en-vi"

    # 1️⃣ Giải nén file LoRA (nếu cần)
    unzip_lora(lora_zip, lora_dir)

    # 2️⃣ Load tokenizer
    print("🔹 Loading tokenizer and base model...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    # 3️⃣ Load base model (use dtype instead of deprecated torch_dtype)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )

    # 4️⃣ Load LoRA adapter (nếu có)
    try:
        from peft import PeftModel
        if os.path.exists(lora_dir) and os.listdir(lora_dir):
            model = PeftModel.from_pretrained(model, lora_dir)
            print(f"✅ LoRA checkpoint loaded successfully from: {lora_dir}")
        else:
            print("⚠️ LoRA directory not found or empty — running base model only.")
    except Exception as e:
        print("⚠️ Could not load LoRA adapter:", e)

    # 5️⃣ Sẵn sàng inference
    model.eval()
    print("✅ Model ready for inference.")
    return model, tokenizer
