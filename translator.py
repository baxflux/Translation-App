import torch

def translate_text(text, model, tokenizer):
    """Dịch tiếng Anh sang tiếng Việt."""
    prompt = f"Translate the following English sentence to Vietnamese. Output ONLY the translation.\nEnglish: {text.strip()}\nVietnamese:"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
            num_beams=1,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            repetition_penalty=2.0
        )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    translation = result.split("Vietnamese:")[-1].strip()
    return translation
