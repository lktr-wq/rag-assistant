# 测试记录

## 1. 基础测试（test_basic.py）

**运行命令**：
```bash
$env:PYTHONIOENCODING="utf-8"; python tests/test_basic.py
```

**测试结果**：9/9 通过

| 测试项 | 结果 |
|--------|------|
| course-faq.md 存在 | ✅ |
| retrieve.py 存在 | ✅ |
| answer.py 存在 | ✅ |
| main.py 存在 | ✅ |
| retrieve 模块可加载 | ✅ |
| answer 模块可加载 | ✅ |
| retrieve() 返回列表 | ✅ |
| answer() 返回 {answer, sources} | ✅ |
| FAQ 文件包含至少 8 个 [faq-XX] 编号 | ✅ |

---

## 2. 功能测试

### 2.1 正确匹配问题

**输入**：`python src/main.py "Day1要交什么？"`

**期望**：返回 6 类证据文件描述，来源为 [faq-02]

**实际输出**：
```
根据课程资料，Day1 最终提交包必须包含 6 类标准文件：
- spec.md：定义要做什么、不做什么、怎么验收
- design.md：技术方案和数据流设计
- ai-log.md：AI 协作决策记录
- test-record.md：测试输入、预期输出、实际输出
- README.md：安装步骤、运行命令、测试命令
- reflection.md：复盘反思

来源: [faq-02]
```

**结果**：✅ 通过

---

### 2.2 跨段落问题

**输入**：`python src/main.py "Spec中的非目标和AI过度设计有什么关系？"`

**期望**：返回多个来源

**实际输出**：
```
非目标是 Spec 的第二要素，明确列出项目不做什么。AI 天然倾向过度设计，没有非目标无法拒绝这些建议。有了非目标，你可以说"这个不在 Spec 的非目标列表里"。

来源: [faq-10], [faq-04]
```

**结果**：✅ 通过

---

### 2.3 资料外问题

**输入**：`python src/main.py "奖学金政策"`

**期望**：返回"资料中没有找到依据"，且不显示任何 `[faq-XX]` 来源

**实际输出**：
```
资料中没有找到依据。
```

**结果**：✅ 通过

**说明**：早期版本曾出现"拒答成功但仍打印来源 [faq-02]"的问题。原因是检索层误召回后，主程序仍使用检索结果附加来源。修复后，拒答结果不再附加来源。

---

### 2.4 混淆问题

**输入**：`python src/main.py "RAG除了关键词还有什么检索方式？"`

**期望**：拒答或正确处理，且拒答时不显示来源编号

**实际输出**：
```
资料中没有找到依据。
```

**结果**：✅ 通过（拒答成功，未显示来源）

---

### 2.5 空输入

**输入**：`python src/main.py`（直接回车）

**期望**：提示"请输入您的问题"

**实际输出**：
```
请输入您的问题。
```

**结果**：✅ 通过

---

## 3. Mock 服务验证

**启动服务**：
```bash
cd llm-mock
python mock_server.py
```

**测试课程相关问题**：
```bash
python -c "import urllib.request, json; req = urllib.request.Request('http://localhost:9876/v1/chat/completions', json.dumps({'model':'mock','messages':[{'role':'user','content':'什么是RAG？'}]}).encode(), {'Content-Type':'application/json'}); print(urllib.request.urlopen(req).read().decode())"
```

**返回结果**：
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "基于课程资料，以下是相关 FAQ 条目的摘要：\n\n1. RAG 是什么？为什么 Day1 要自己实现 RAG？\n2. Day1 的工具链是什么？\n\n来源: [faq-05], [faq-06]"
    }
  }]
}
```

**结果**：✅ 通过

---

## 4. MiMo API 验证

**配置**：
- API Base：`https://api.xiaomimimo.com/v1/chat/completions`
- Model：`mimo-v2.5-pro`
- API Key：本地测试时通过环境变量配置；公开提交版本已移除真实密钥

**测试课程相关问题**：
```bash
python src/main.py "什么是RAG？"
```

**返回结果**：
```
RAG（检索增强生成）是"检索增强生成"，先检索相关资料，再把资料和问题一起发给 LLM，让 LLM 基于资料回答。

来源: [faq-05]
```

**结果**：✅ 通过

---

## 测试总结

| 测试类别 | 测试数量 | 通过数量 | 失败数量 |
|---------|---------|---------|---------|
| 基础测试 | 9 | 9 | 0 |
| 功能测试 | 5 | 5 | 0 |
| Mock 服务 | 1 | 1 | 0 |
| MiMo API | 1 | 1 | 0 |
| **总计** | **16** | **16** | **0** |

**结论**：全部测试通过，RAG 课程助手功能完整。
