# CLAUDE.md — AI 协作指南

## 项目

Day1 RAG 课程助手，基于 `data/course-faq.md` 的 CLI 问答工具。

## 约束

- 仅基于 `course-faq.md` 回答问题
- 资料外问题必须拒答，不能编造
- 不引入数据库或外部存储
- CLI 工具，不支持 Web UI
- 回答必须注明来源 `[faq-XX]`

## 接口

- `parse_faq(filepath) -> list[dict]`：将 FAQ 文件切分为 chunk 列表
- `retrieve(query, chunks) -> list[dict]`：检索相关 chunks
- `answer(query, chunks) -> dict`：生成回答，返回 `{"answer": "...", "sources": [...]}`

## 运行

```bash
python src/main.py "Day1要交什么？"
python tests/test_basic.py
```
