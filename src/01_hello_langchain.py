# -*- coding: utf-8 -*-
# 第一个 LangChain 练手：prompt | llm，连本地 Ollama
# 运行：python src/01_hello_langchain.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen3.5:4b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个简洁的技术学习助手，回答不超过两句话。"),
    ("human", "用一句话给初学者解释什么是{name}。"),
])

chain = prompt | llm

if __name__ == "__main__":
    for name in ("RAG", "LangChain"):
        resp = chain.invoke({"name": name})
        print(f"Q: 什么是{name}")
        print(f"A: {resp.content}\n")
