# RAG 课程助手 — 实现计划

## 总体数据流

```
course-faq.md → 切片(parse_faq) → 检索(retrieve) → Prompt拼接 → LLM生成 → 来源引用+拒答
```

---

## S3：阅读知识库，写 Spec

**任务**：
1. 阅读 `data/course-faq.md`，理解 10 条 FAQ 的结构和内容
2. 创建 `docs/spec.md`，包含：
   - **目标（Goals）**：CLI 问答、基于 course-faq、资料外拒答、来源引用
   - **非目标（Non-Goals）**：无 Web UI、无数据库、无外部依赖
   - **验收标准**：输入输出示例、测试通过标准

**Git 提交**：
```bash
git add docs/spec.md
git commit -m "S3: 添加 RAG 课程助手规格说明"
```

---

## S4：创建项目骨架，写 README + CLAUDE.md

**任务**：
1. 创建目录结构：
   ```
   src/
   ├── __init__.py
   ├── retrieve.py    # 空签名
   ├── answer.py      # 空签名
   └── main.py        # 空签名
   docs/
   └── design.md      # 空文件
   ```
2. 创建 `CLAUDE.md`：项目上下文、约束、接口说明、运行命令

**Git 提交**：
```bash
git add src/ CLAUDE.md
git commit -m "S4: 创建项目目录骨架和 CLAUDE.md"
```

---

## S5：定义接口契约，写 main.py 骨架

**任务**：
1. 在 `src/retrieve.py` 定义空签名：
   ```python
   def parse_faq(filepath: str) -> list[dict]:
       """将 FAQ 文件切分为 chunk 列表。"""
       raise NotImplementedError

   def retrieve(query: str, chunks: list, top_k: int = 3) -> list[dict]:
       """检索与 query 最相关的 chunks。"""
       raise NotImplementedError
   ```

2. 在 `src/answer.py` 定义空签名：
   ```python
   def answer(query: str, chunks: list) -> dict:
       """生成回答。返回 {"answer": "...", "sources": ["[faq-XX]"]}"""
       raise NotImplementedError
   ```

3. 在 `src/main.py` 写 CLI 骨架：
   ```python
   import sys
   from src.retrieve import parse_faq
   from src.answer import answer

   def main():
       query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else input("请输入问题: ")
       # TODO: 调用 parse_faq + answer
       print(f"问题: {query}")

   if __name__ == '__main__':
       main()
   ```

4. 验证：`python tests/test_basic.py` 的模块加载和接口检查通过

**Git 提交**：
```bash
git add src/
git commit -m "S5: 定义接口契约和 main.py 骨架"
```

---

## S6：设计 RAG 数据流，启动 llm-mock 测试

**任务**：
1. 编写 `docs/design.md`，包含：
   - **数据流图**：course-faq.md → parse_faq → retrieve → Prompt → LLM → 输出
   - **检索策略**：关键词匹配、分词方案、评分公式、标题加权
   - **拒答逻辑**：三道防线（空输入、无结果、低分）
   - **Prompt 模板**：System 指令 + 检索上下文 + 用户问题

2. 启动 Mock 服务验证：
   ```bash
   cd llm-mock
   python mock_server.py
   # 新终端测试
   curl http://localhost:9876/v1/chat/completions -H "Content-Type: application/json" -d '{"model":"mock","messages":[{"role":"user","content":"什么是RAG？"}]}'
   ```

**Git 提交**：
```bash
git add docs/design.md
git commit -m "S6: 添加 RAG 数据流设计文档"
```

---

## S7：实现检索和回答模块，跑通全部测试

**任务**：

1. **实现 `src/retrieve.py`**：
   - `parse_faq()`：正则切片 `##\s*\[(faq-\d{2})\]`
   - `tokenize()`：中文 2-gram + 英文空格分词
   - `retrieve()`：TF 匹配 + 标题加权 + 阈值过滤

2. **实现 `src/answer.py`**：
   - 拒答逻辑：空输入 / 无结果 / 低分
   - Prompt 模板：强制"只基于资料回答"
   - LLM 调用：`urllib.request` POST 到 Mock 服务
   - 来源提取：从检索结果中提取 `[faq-XX]`

3. **完善 `src/main.py`**：
   - 调用 `parse_faq()` → `answer()` → 输出结果和来源

4. **运行测试验证**：
   ```bash
   python tests/test_basic.py
   python src/main.py "Day1要交什么？"      # 期望：答案 + [faq-02]
   python src/main.py "奖学金政策？"         # 期望：拒答
   python src/main.py ""                     # 期望：提示输入
   ```

**Git 提交**：
```bash
git add src/
git commit -m "S7: 实现检索和回答模块，跑通全部测试"
```

---

## S8：工程交付证据链完备

**任务**：完善交付所需的 6 类证据文件

| 文件 | 状态 | 行动 |
|------|------|------|
| `docs/spec.md` | 已存在 | 检查完善 |
| `docs/design.md` | 已存在 | 检查完善 |
| `docs/ai-log.md` | 不存在 | 根据备份总结创建 |
| `docs/test-record.md` | 不存在 | 根据测试结果创建 |
| `docs/README.交付版.md` | 不存在 | 创建交付版 README |
| `docs/reflection.md` | 不存在 | 复盘反思 |

**Git 提交**：
```bash
git add docs/
git commit -m "S8: 工程交付证据链完备"
```

---

## S9：提交前检查，复盘反思

**任务**：
1. 运行完整测试套件：
   ```bash
   python tests/test_basic.py
   ```

2. 手动验证五类问题（questions.json）：
   - 正确匹配 → 返回答案 + 来源
   - 跨段落 → 返回多个来源
   - 资料外 → 拒答
   - 混淆 → 拒答
   - 空输入 → 提示

3. 检查代码规范：
   - 无硬编码路径
   - 无多余依赖
   - 接口契约一致

4. 最终提交：
   ```bash
   git add -A
   git commit -m "S9: 完成 RAG 课程助手，通过全部测试"
   ```

---

## 调优关键点

| 参数 | 作用 | 建议值 |
|------|------|--------|
| `RELEVANCE_THRESHOLD` | 拒答阈值 | 0.15（太低误答，太高拒答） |
| 标题加权系数 | 标题匹配额外加分 | 0.3 |
| `top_k` | 返回结果数量 | 3（跨段落问题需 ≥2） |
