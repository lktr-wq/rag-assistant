import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.retrieve import parse_faq
from src.answer import answer


def extract_and_remove_sources(text: str) -> tuple[str, list[str]]:
    """从模型回答中提取来源编号，并从文本中删除来源部分。"""
    sources = re.findall(r'\[faq-\d{2}\]', text)
    # 删除包含"来源"的行（支持 Markdown 格式）
    text = re.sub(r'^.*来源.*$', '', text, flags=re.MULTILINE).strip()
    return text, sources


def main():
    faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'course-faq.md')
    chunks = parse_faq(faq_path)

    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("请输入您的问题: ")

    result = answer(query, chunks)

    answer_text, sources = extract_and_remove_sources(result['answer'])
    print(f"\n{answer_text}")

    if not sources:
        sources = result['sources']
    if sources:
        print(f"\n来源: {', '.join(sources)}")


if __name__ == '__main__':
    main()
