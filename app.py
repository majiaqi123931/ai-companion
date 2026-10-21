import streamlit as st
from openai import OpenAI
import os
from datetime import datetime
import json

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="👾",
    # 布局
    layout="wide",
    initial_sidebar_state="expanded"
)

# 保存会话信息
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 如果sessions文件夹不存在则创建
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        # 保存会话信息
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

# 生成会话标识函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 加载所有会话信息
def load_sessions():
    session_list=[]
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    return session_list

def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name

    except Exception as e:
        st.error(f"加载会话失败: {e}")

# 删除会话信息函数
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
        # 如果删除的是当前会话，更新消息列表
        if session_name == st.session_state.current_session:
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error(f"删除会话失败: {e}")

# 创建与AI大模型交互的客户端
client = OpenAI(
    api_key=os.environ.get("LLM_API_KEY", "ollama"),  # 本地 Ollama 随意填；接云端 API 时改成环境变量
    base_url=os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1"))

# 系统提示词
system_prompt = """
    你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。
    规则：
        1．每次只回1条消息
        2．可以包含任何场景或状态描述性文字
        3．匹配用户的语言
        4．回复简短，像微信聊天一样
        5．有需要的话可以用❤🌸等emoji表情
        6．用符合伴侣性格的方式对话
        7．回复的内容，要充分体现伴侣的性格特征
    伴侣性格：
        - %s
    你必须严格遵守上述规则来回复用户。
"""

# 初始化聊天信息
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "小美"

if 'nature' not in st.session_state:
    st.session_state.nature = "甜美的四川妹子"

if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


# 侧边栏
with st.sidebar:
    st.subheader("AI控制面板")

    if st.button("新建会话",width="stretch",icon="✏️"):
        # 保存当前会话信息
        save_session()

        if st.session_state.messages:
            # 新建会话信息
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()

            save_session()
            st.rerun()

    # 会话历史
    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            if st.button(session,width="stretch",icon="📄",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("",width="stretch",icon="❌",key=f"delete_{session}"):
                delete_session(session)
                st.rerun()


    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("性格",placeholder="请输入性格",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature
# 大标题
st.title("AI智能伴侣")

# logo
st.logo("./img.png")

st.text(f"会话名称：{st.session_state.current_session}")

# 展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 消息输入框
prompt = st.chat_input("请输入您的问题")
if prompt:
    st.chat_message("user").write(prompt)
    # 保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})


    # 与AI大模型交互
    response = client.chat.completions.create(
        model=os.environ.get("LLM_MODEL", "qwen3.5:4b"),
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="none",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 流式输出
    response_message = st.empty()
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)


    # 保存AI大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    save_session()
