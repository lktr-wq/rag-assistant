# Mock 服务验证记录

## 验证时间
S6 阶段

## 验证步骤

### 1. 启动 Mock 服务
```bash
cd llm-mock
python mock_server.py
```

服务启动后显示：
```
已加载 FAQ 文件: ../data/course-faq.md
LLM Mock Server running at http://localhost:9876
API endpoint: http://localhost:9876/v1/chat/completions
```

### 2. 测试课程相关问题
```bash
python -c "import urllib.request, json; req = urllib.request.Request('http://localhost:9876/v1/chat/completions', json.dumps({'model':'mock','messages':[{'role':'user','content':'什么是RAG？'}]}).encode(), {'Content-Type':'application/json'}); print(urllib.request.urlopen(req).read().decode())"
```

返回结果：
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

### 3. 测试资料外问题
```bash
python -c "import urllib.request, json; req = urllib.request.Request('http://localhost:9876/v1/chat/completions', json.dumps({'model':'mock','messages':[{'role':'user','content':'奖学金政策'}]}).encode(), {'Content-Type':'application/json'}); print(urllib.request.urlopen(req).read().decode())"
```

返回结果：
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "资料中没有找到依据。本助手仅能回答 Day1 AI Native 训练营相关问题。"
    }
  }]
}
```

## 验证结论

Mock 服务正常工作：
- 能正确加载 course-faq.md 知识库
- 能区分课程相关和资料外问题
- 课程相关问题返回 FAQ 摘要和来源引用
- 资料外问题返回拒答信息
- API 格式兼容 OpenAI Chat Completions API

## 备注

Windows 终端中文显示乱码是编码问题，JSON 结构和功能完全正常。
