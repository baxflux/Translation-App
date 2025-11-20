import re
from typing import List
from transformers import PreTrainedTokenizer

_SENTENCE_SPLIT_REGEX = re.compile(r'(?<=[.!?])\s+')

def split_into_sentences(text: str) -> List[str]:
    sentences = _SENTENCE_SPLIT_REGEX.split(text)
    return [s.strip() for s in sentences if s.strip()]

def build_chunks(
    sentences: List[str],
    tokenizer: PreTrainedTokenizer,
    max_tokens: int
) -> List[str]:
    chunks = []
    current_chunk = []
    current_tokens = 0

    for sent in sentences:
        sent_token_ids = tokenizer(
            sent,
            add_special_tokens=False
        )["input_ids"]
        sent_len = len(sent_token_ids)

        if sent_len > max_tokens:
            truncated = sent_token_ids[:max_tokens]
            chunks.append(
                tokenizer.decode(truncated, skip_special_tokens=True)
            )
            continue

        if current_tokens + sent_len > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sent]
            current_tokens = sent_len
        else:
            current_chunk.append(sent)
            current_tokens += sent_len

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
