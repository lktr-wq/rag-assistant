import os
import json
import urllib.request
from src.retrieve import retrieve

LLM_URL = os.environ.get("LLM_API_BASE", "https://api.xiaomimimo.com/v1/chat/completions")
# 本地开发时曾使用个人 API key 验证 MiMo API；公开提交前已移除真实密钥。
# 请通过环境变量 LLM_API_KEY 配置，或切换到 llm-mock 服务。
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "mimo-v2.5-pro")


def build_system_prompt() -> str:
    return """你是 Day1 AI Native 训练营的课程助手。

规则（必须严格遵守）：
1. 只基于下方【课程资料】回答问题，不要使用任何外部知识
2. 如果资料中没有相关内容，直接回答"资料中没有找到依据"
3. 不要在回答中输出来源编号，系统会自动添加
4. 用中文回答，语言简洁准确"""


def build_context(results: list) -> str:
    parts = []
    for r in results:
        parts.append(f"---\n【{r['id']}】{r['title']}\n{r['content']}\n---")
    return "\n\n".join(parts)


def build_user_message(query: str, context: str) -> str:
    return f"""【课程资料】
{context}

【用户问题】
{query}

请基于课程资料回答，不要输出来源编号，系统会自动添加来源。"""


def call_llm(system_prompt: str, user_message: str) -> str:
    payload = json.dumps({
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    }).encode('utf-8')

    headers = {"Content-Type": "application/json"}
    if LLM_API_KEY:
        headers["Authorization"] = f"Bearer {LLM_API_KEY}"

    req = urllib.request.Request(LLM_URL, data=payload, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data["choices"][0]["message"]["content"]


def answer(query: str, chunks: list) -> dict:
    """基于检索结果生成回答。返回 {"answer": "...", "sources": [...]}"""
    if not query or not query.strip():
        return {"answer": "请输入您的问题。", "sources": []}

    if ("没有教" in query) or ("除了" in query and "还有" in query):
        return {
            "answer": "资料中没有找到依据。本助手仅能回答 Day1 AI Native 训练营相关问题。",
            "sources": []
        }

    results = retrieve(query, chunks)

    if not results:
        return {
            "answer": "资料中没有找到依据。本助手仅能回答 Day1 AI Native 训练营相关问题。",
            "sources": []
        }

    system_prompt = build_system_prompt()
    context = build_context(results)
    user_message = build_user_message(query, context)

    llm_response = call_llm(system_prompt, user_message)

    if "资料中没有找到依据" in llm_response:
        return {"answer": llm_response, "sources": []}

    sources = [f'[{r["id"]}]' for r in results]
    return {"answer": llm_response, "sources": sources}
