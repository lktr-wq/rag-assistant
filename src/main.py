import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.retrieve import parse_faq
from src.answer import answer


def main():
    faq_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'course-faq.md')
    chunks = parse_faq(faq_path)

    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        query = input("请输入您的问题: ")

    result = answer(query, chunks)

    print(f"\n{result['answer']}")
    if result['sources']:
        print(f"\n来源: {', '.join(result['sources'])}")


if __name__ == '__main__':
    main()
