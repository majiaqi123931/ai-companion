# 01 跑通第一个 LangChain 程序

10.21 装了 langchain 1.4.6 和 langchain-ollama，照官方 quickstart 改了个最小例子：ChatPromptTemplate 加 ChatOllama，中间用 | 连起来就是一条链。模型用的本地 ollama 的 qwen3.5:4b，不用 api key。

```
python src/01_hello_langchain.py
```

输出：

```
Q: 什么是RAG
A: RAG（检索增强生成）是一种让大模型先搜索外部知识库再回答问题，从而减少"幻觉"并提升准确性的技术。

Q: 什么是LangChain
A: LangChain 是一个开发框架，用于将大语言模型与外部工具（如数据库、API）连接起来，从而简化复杂 AI 应用的构建。
```

两个感受：一是比直接裸调 openai sdk 多了层抽象，以后换模型应该只改一处；二是 system 里写"不超过两句话"确实管用，输出没废话。

下一步看下 output parser，然后试着把链塞进 AI 伴侣里。
