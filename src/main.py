import sys


def main():
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else input("请输入问题: ")
    # TODO: 调用 parse_faq + answer
    print(f"问题: {query}")


if __name__ == '__main__':
    main()
