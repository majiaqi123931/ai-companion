# AI 智能伴侣

基于大模型的角色扮演聊天应用：可以自定义伴侣的昵称和性格，支持多轮对话、流式输出和会话管理。默认连本地 Ollama，改环境变量就能切到其他 OpenAI 兼容的云端 API。

![screenshot](docs/screenshot.png)

## 功能

- 多轮对话，回答流式输出
- 昵称 / 性格可配置，通过 System Prompt 动态生效
- 会话自动保存成 JSON，支持加载和删除
- OpenAI 兼容接口，本地 Ollama 和云端 API 可以切换

## 开发过程

项目是跟着课程一步步做出来的：v1 只能单轮对话（DeepSeek API），v2 换成本地 Ollama 并加了流式输出，v3 加了人设配置，v4 加了会话管理（保存 / 加载 / 删除）。

## 运行

```
pip install -r requirements.txt
ollama pull qwen3.5:4b
streamlit run app.py
```

默认连接 http://localhost:11434/v1，模型 qwen3.5:4b。想换 DeepSeek：

```
$env:LLM_API_KEY = "sk-你的密钥"
$env:LLM_BASE_URL = "https://api.deepseek.com"
$env:LLM_MODEL = "deepseek-chat"
```

环境变量说明见 `.env.example`。

## 接下来

准备把它改成 RAG 版：接入课程资料做知识库，回答带上引用来源，过程记录在 notes/ 目录。

---

柯润杭 · 广东白云学院 · 计算机科学与技术
