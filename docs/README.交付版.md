# RAG 课程助手 — 交付版 README

## 项目简介

Day1 AI Native 训练营的 RAG 课程助手，基于 `data/course-faq.md` 的 CLI 问答工具。

## 目录结构

```
rag-assistant/
├── data/
│   └── course-faq.md       # 知识库（10 条 FAQ）
├── src/
│   ├── __init__.py
│   ├── retrieve.py          # 检索模块
│   ├── answer.py            # 回答模块
│   └── main.py              # CLI 入口
├── docs/
│   ├── spec.md              # 规格说明
│   ├── design.md            # 设计文档
│   ├── ailog.md             # AI 协作日志
│   ├── testrecord.md        # 测试记录
│   ├── README.交付版.md      # 本文件
│   └── reflection.md        # 复盘反思
├── tests/
│   ├── test_basic.py        # 基础测试
│   └── questions.json       # 测试问题
├── llm-mock/
│   ├── mock_server.py       # Mock 服务
│   └── README.md
├── README.md
├── CLAUDE.md
└── PLAN.md
```

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/lktr-wq/rag-assistant.git
cd rag-assistant
```

2. 配置环境变量（可选，使用 MiMo API）：
```bash
export LLM_API_BASE=https://api.xiaomimimo.com/v1/chat/completions
export LLM_API_KEY=your-api-key
export LLM_MODEL=mimo-v2.5-pro
```

## 运行命令

### 使用 MiMo API（默认）
```bash
python src/main.py "Day1要交什么？"
python src/main.py "什么是可复核交付？"
python src/main.py "奖学金政策"  # 应拒答
```

### 使用 Mock 服务
```bash
# 终端 1：启动 Mock 服务
cd llm-mock
python mock_server.py

# 终端 2：运行 RAG 助手
$env:LLM_API_BASE="http://localhost:9876/v1/chat/completions"
$env:LLM_API_KEY="mock-key"
$env:LLM_MODEL="mock"
python src/main.py "什么是RAG？"
```

## 测试命令

```bash
# 运行基础测试
$env:PYTHONIOENCODING="utf-8"; python tests/test_basic.py

# 测试各类问题
python src/main.py "Day1要交什么？"           # 正确匹配
python src/main.py "Spec中的非目标和AI过度设计"  # 跨段落
python src/main.py "奖学金政策"                # 资料外拒答
python src/main.py                           # 空输入
```

## 核心功能

1. **检索**：基于关键词 TF 匹配 + 标题加权
2. **回答**：调用 MiMo-V2.5-Pro API 生成回答
3. **来源引用**：回答末尾注明来源 [faq-XX]
4. **资料外拒答**：问题与资料无关时拒绝回答

## 依赖

- Python 3.x
- 无外部依赖（仅使用标准库）

## 约束

- CLI 工具，不支持 Web UI
- 不引入数据库或外部存储
- 仅基于 `course-faq.md` 回答问题
- 资料外问题必须拒答

## 交付证据

| 文件 | 说明 |
|------|------|
| `docs/spec.md` | 规格说明（目标/非目标/验收标准） |
| `docs/design.md` | 设计文档（数据流/检索策略/Prompt 模板） |
| `docs/ailog.md` | AI 协作日志（目的/输入/建议/判断/验证） |
| `docs/testrecord.md` | 测试记录（基础测试/功能测试/Mock 验证/API 验证） |
| `docs/README.交付版.md` | 交付版 README（本文件） |
| `docs/reflection.md` | 复盘反思 |
