import re


def parse_faq(filepath: str) -> list[dict]:
    """将 FAQ 文件切分为 chunk 列表。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    pattern = r'##\s*\[(faq-\d{2})\]\s*(.*?)(?=\n##\s*\[faq-|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    chunks = []
    for faq_id, body in matches:
        lines = body.strip().split('\n')
        title = lines[0].strip()
        content = body.strip()
        chunks.append({"id": faq_id, "title": title, "content": content})
    return chunks


def tokenize(text: str) -> list[str]:
    """简单分词：中文按 2-gram，英文按空格+小写。"""
    text = text.lower()
    cn_chars = re.findall(r'[\u4e00-\u9fff]', text)
    en_words = re.findall(r'[a-z0-9]+', text)

    cn_bigrams = [cn_chars[i] + cn_chars[i+1] for i in range(len(cn_chars)-1)]
    tokens = cn_chars + cn_bigrams + en_words
    return tokens


def retrieve(query: str, chunks: list, top_k: int = 3, threshold: float = 0.15) -> list[dict]:
    """检索与 query 最相关的 chunks。返回按 score 降序的结果。"""
    if not query or not query.strip():
        return []
    if not chunks:
        return []

    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scored = []
    for chunk in chunks:
        chunk_text = chunk["title"] + " " + chunk["content"]
        chunk_tokens = tokenize(chunk_text)

        hits = sum(1 for t in query_tokens if t in chunk_tokens)
        score = hits / len(query_tokens)

        title_tokens = tokenize(chunk["title"])
        title_hits = sum(1 for t in query_tokens if t in title_tokens)
        if title_hits > 0:
            score += 0.3 * (title_hits / len(query_tokens))

        scored.append({**chunk, "score": round(score, 4)})

    scored = [s for s in scored if s["score"] > threshold]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
