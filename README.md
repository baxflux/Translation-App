# Translation-App

Ứng dụng dịch tiếng Anh → tiếng Việt đơn giản sử dụng mô hình Qwen + LoRA. Ứng dụng chạy một server Flask nhỏ với giao diện web và API HTTP để gửi văn bản tiếng Anh và nhận về bản dịch tiếng Việt.

**Tóm tắt**:

- **Ngôn ngữ:** Python
- **Framework web:** `Flask`
- **Model:** base `Qwen/Qwen2.5-0.5B` với tùy chọn LoRA adapter trong `model/qwen2.5-lora-en-vi`.

**Cấu trúc dự án**

- `app.py`: entrypoint Flask; định nghĩa route `/` (giao diện) và `/translate` (API JSON).
- `model_loader.py`: chứa hàm `load_model()` và tiện ích `unzip_lora()` để giải nén LoRA (nếu có) và load tokenizer + model.
- `translator.py`: hàm `translate_text(text, model, tokenizer)` tạo prompt, gọi `model.generate()` và trích xuất kết quả dịch.
- `templates/index.html`: giao diện web đơn giản (textarea + nút Translate) gọi API `/translate`.
- `static/style.css`: kiểu cho giao diện (nội dung CSS).
- `model/`: chứa checkpoint LoRA và các file liên quan (ví dụ `qwen2.5-lora-en-vi/adapter_model.safetensors`, `tokenizer.json`, ...).

**Yêu cầu (khuyến nghị)**

- Python 3.8+ (hoặc tương đương đã được kiểm tra với PyTorch/Transformers)
- GPU với CUDA để chạy mô hình lớn hiệu quả (nếu không có GPU, model có thể rất chậm hoặc không chạy được do cấu hình `device_map="auto"`).
- Thư viện Python chính:
  - `torch`
  - `transformers`
  - `peft` (tùy chọn, để load LoRA)
  - `flask`

Có thể cài nhanh bằng pip (PowerShell):

```powershell
python -m pip install -U pip
python -m pip install torch transformers peft flask
```

Lưu ý: Cách cài `torch` chính xác tùy thuộc vào platform và phiên bản CUDA; xem hướng dẫn chính thức tại `https://pytorch.org`.

**Cách chạy (local)**

- Đảm bảo đã đặt các file mô hình trong thư mục `model/`. Nếu có file LoRA zip (ví dụ `model/qwen2.5-lora.zip`), `model_loader.unzip_lora()` sẽ giải nén vào `model/qwen2.5-lora-en-vi` khi khởi động.
- Chạy server Flask:

```powershell
python app.py
```

- Mở trình duyệt tới `http://localhost:8080` để sử dụng giao diện web.
