# 01 | 第一次跑通 LangChain（2026-10-21）

## 今天做了什么

- 安装 `langchain`（1.4.6）和 `langchain-ollama`
- 写了第一个 LCEL 程序 `src/01_hello_langchain.py`：`ChatPromptTemplate | ChatOllama`，连本地 Ollama 的 qwen3.5:4b 直接就跑通了，不用 API key、不花钱

## 运行记录

```bash
pip install langchain langchain-ollama
python src/01_hello_langchain.py
```

真实输出：

```
Q: 什么是RAG
A: RAG（检索增强生成）是一种让大模型先搜索外部知识库再回答问题，从而减少"幻觉"并提升准确性的技术。

Q: 什么是LangChain
A: LangChain 是一个开发框架，用于将大语言模型与外部工具（如数据库、API）连接起来，从而简化复杂 AI 应用的构建。
```

## 三个收获

1. Chain 的本质就是"提示词模板 + 模型"用 `|` 串起来，比在 AI 伴侣里直接裸调 OpenAI SDK 多了一层可组合的抽象，以后换模型、换提示词都只动一处
2. `ChatOllama` 走的也是 OpenAI 兼容那套本地接口（11434），以后想切云端模型只要换个模型类，业务代码不动
3. system 里限"不超过两句话"真的有用——写提示词要给明确约束

## 下一步

- 看官方 Quickstart 的 Output Parser（结构化输出）
- 把这个 Chain 塞进 AI 伴侣里试水，为 RAG 化改造热身
