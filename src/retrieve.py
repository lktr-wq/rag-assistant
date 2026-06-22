def parse_faq(filepath: str) -> list[dict]:
    """将 FAQ 文件切分为 chunk 列表。"""
    raise NotImplementedError


def retrieve(query: str, chunks: list, top_k: int = 3) -> list[dict]:
    """检索与 query 最相关的 chunks。"""
    return []
