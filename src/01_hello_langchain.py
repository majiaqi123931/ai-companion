# -*- coding: utf-8 -*-
"""第一次跑通 LangChain：本地 Ollama (qwen3.5:4b) + LCEL 最小 Chain

运行：python src/01_hello_langchain.py
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 模型：复用 AI 伴侣项目里已装好的本地 Ollama，不花钱
llm = ChatOllama(model="qwen3.5:4b")

# 提示词模板：system 定角色，human 收变量
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的技术学习助手，回答不超过两句话。"),
    ("human", "用一句话给初学者解释什么是{name}。"),
])

# LCEL：用 | 把提示词和模型串成一条链
chain = prompt | llm

if __name__ == "__main__":
    for name in ("RAG", "LangChain"):
        resp = chain.invoke({"name": name})
        print(f"Q: 什么是{name}")
        print(f"A: {resp.content}\n")
