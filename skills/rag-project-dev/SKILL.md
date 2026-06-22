# RAG 项目开发最佳实践

## 核心理念：螺旋上升与全程溯源

### 螺旋上升

项目的完成是螺旋上升的过程：

1. **先框架后细化**：先做出大致框架（空文件骨架），再逐一填充实现
2. **反思即 Skill**：项目完成后的反思可以总结为 Skill，Skill 又可以指导该项目的维护与类似项目的开发
3. **迭代优化**：每一轮迭代都在前一轮基础上提升，而不是推倒重来

**实践路径**：
```
S3: 写 Spec（定义边界）
  ↓
S4: 创建骨架（空文件）
  ↓
S5: 定义接口（空签名）
  ↓
S6: 设计文档（检索策略、Prompt 模板）
  ↓
S7: 实现功能（检索、回答、CLI）
  ↓
S8: 交付证据（ailog、testrecord、reflection）
  ↓
S9: 测试验证（基础测试、功能测试）
  ↓
反思 → 总结为 Skill → 指导下一轮开发
```

### 全程溯源

每一步都应该可以溯源，体现在：

1. **Git 提交记录**：每一步都有明确的提交信息，记录"做了什么"和"为什么这样做"
2. **PLAN.md**：记录完整的计划和执行过程，每一步都有对应的任务和提交
3. **ailog.md**：记录 AI 协作的决策过程，每条记录包含目的、输入、建议、人工判断、验证
4. **testrecord.md**：记录测试验证过程，每个测试都有输入、期望输出、实际输出
5. **reflection.md**：记录反思和总结，包括认知变化、遇到的困难、改进方向

**溯源的价值**：
- 助教可以独立判断你的工作质量
- 未来的你可以理解当时的决策逻辑
- 其他人可以从你的经验中学习

---

## Git 管理最佳实践

### 提交策略

1. **每完成一个任务先确认再 push**
   - 告诉用户完成了什么
   - 等用户确认后再 git push
   - 避免"先写后删"的尴尬历史

2. **空文件骨架和接口签名分开提交**
   - S4：只提交空文件（骨架）
   - S5：提交接口签名（函数定义）
   - S5-2：提交测试修复（返回空值）

3. **提交信息要详细**
   - 不要只写"update"或"fix"
   - 要说明"做了什么"和"为什么这样做"
   - 例如："S5-2: 修复接口契约，retrieve() 返回空列表，answer() 返回空字典"

### 重写历史

如果需要重写历史（例如删除错误提交）：

```bash
# 回退到指定提交
git reset --soft <commit-hash>

# 重新提交
git add .
git commit -m "新的提交信息"

# 强制推送
git push --force
```

**注意**：强制推送会覆盖远程历史，确保本地是正确的。

---

## 接口契约设计

### 先看测试再写实现

1. **阅读 test_basic.py**：了解函数签名和返回类型要求
2. **定义空签名**：先写函数定义，抛出 NotImplementedError
3. **实现功能**：根据测试要求实现具体逻辑
4. **运行测试**：确保测试通过

### 空值返回比 NotImplementedError 更安全

```python
# 不推荐：测试会失败
def retrieve(query, chunks):
    raise NotImplementedError

# 推荐：测试会通过
def retrieve(query, chunks):
    return []

# 推荐：测试会通过
def answer(query, chunks):
    return {"answer": "", "sources": []}
```

### 接口签名要严格匹配测试期望

```python
# 测试要求 retrieve() 返回 list
def retrieve(query: str, chunks: list, top_k: int = 3) -> list[dict]:
    return []

# 测试要求 answer() 返回 dict 含 answer 和 sources
def answer(query: str, chunks: list) -> dict:
    return {"answer": "", "sources": []}
```

---

## RAG 开发最佳实践

### 检索策略要匹配场景规模

- **小规模（<100 条）**：关键词匹配足够
- **中等规模（100-10000 条）**：TF-IDF 或 BM25
- **大规模（>10000 条）**：向量检索（embedding）

**本项目**：10 条 FAQ，使用中文 2-gram + 标题加权即可。

### 拒答逻辑需要程序兜底

不能完全依赖 LLM 遵循指令，需要三道防线：

1. **空输入**：query 为空或纯空格 → 提示用户
2. **无检索结果**：retrieve() 返回空列表 → 直接拒答
3. **低分结果**：最高分 < 阈值 → 直接拒答

```python
def answer(query, chunks):
    if not query or not query.strip():
        return {"answer": "请输入您的问题。", "sources": []}

    results = retrieve(query, chunks)
    if not results:
        return {"answer": "资料中没有找到依据。", "sources": []}

    # 调用 LLM
    ...
```

### 来源引用要从模型回答中提取

LLM 可能不遵循指令，需要程序逻辑保证：

```python
import re

def extract_and_remove_sources(text):
    """从模型回答中提取来源编号，并删除来源部分。"""
    sources = re.findall(r'\[faq-\d{2}\]', text)
    text = re.sub(r'^.*来源.*$', '', text, flags=re.MULTILINE).strip()
    return text, sources
```

---

## 用户沟通最佳实践

### 详细说明修改内容

不要只说"已修改"，要说明：
- 修改了哪个文件
- 修改了什么内容
- 为什么这样修改

### 按照学习路径执行

如果用户提供了学习路径（如 S3-S8），严格按照路径执行，不要跳步。

### 同步确认后再上传

每完成一个任务，先告诉用户完成了什么，等用户确认后再 git push。

---

## 常见问题和解决方案

### 1. Windows 终端编码问题

**问题**：Python 输出中文乱码

**解决**：
```bash
$env:PYTHONIOENCODING="utf-8"; python script.py
```

### 2. Git 用户配置

**问题**：提交时提示 "Author identity unknown"

**解决**：
```bash
git config user.email "your-email@example.com"
git config user.name "Your Name"
```

### 3. 来源重复显示

**问题**：模型回答中输出来源，main.py 又打印一次来源

**解决**：从模型回答中提取来源，删除回答中的来源部分

### 4. Mock 服务和 API 切换

**问题**：切换 Mock 服务和实际 API 不方便

**解决**：使用环境变量配置
```bash
$env:LLM_API_BASE="http://localhost:9876/v1/chat/completions"
$env:LLM_API_KEY="mock-key"
$env:LLM_MODEL="mock"
```

---

## Skill 的价值

这个 Skill 记录了 RAG 项目开发的最佳实践，可以用于：

1. **指导本项目的维护**：未来的你可以参考这些实践来维护项目
2. **指导类似项目的开发**：其他人可以参考这些实践来开发类似的 RAG 项目
3. **总结和反思**：通过写 Skill，你可以更深入地理解项目中的经验教训

**螺旋上升的体现**：
- 项目完成 → 反思 → 总结为 Skill → 指导下一轮开发
- 每一轮都在前一轮基础上提升
