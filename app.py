import streamlit as st
import os
import sys
import tempfile
import chromadb
import numpy as np
from fastembed.embedding import TextEmbedding
from openai import OpenAI
from dotenv import load_dotenv
import hashlib

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(dotenv_path=r"D:\SystemData\Python\damoxing\.env", override=True)

st.set_page_config(page_title="Python RAG 知识库", page_icon="📚")

# === 配置 ===
DB_PATH = r"D:\SystemData\Python\damoxing\.vectorstore"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBED_MODEL = None

def get_embed_model():
    global EMBED_MODEL
    if EMBED_MODEL is None:
        EMBED_MODEL = TextEmbedding(model_name=MODEL_NAME)
    return EMBED_MODEL

def get_embedding(text):
    return next(np.array(e, dtype=np.float32) for e in get_embed_model().embed([text])).tolist()

def load_db():
    return chromadb.PersistentClient(path=DB_PATH).get_collection(name="python_docs")

# 千问客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
)

# === 侧边栏 ===
with st.sidebar:
    st.title("📚 Python RAG")
    st.markdown("上传 Python 文档，自动建库问答")
    
    if st.button("🔄 重建知识库"):
        st.session_state["rebuild"] = True
        st.rerun()
    
    # 加载现有知识库
    if "db" not in st.session_state:
        try:
            st.session_state["db"] = load_db()
            st.success("✅ 知识库已加载")
        except Exception as e:
            st.error(f"❌ 知识库加载失败: {e}")

# === 主页面 ===
st.title("📚 Python RAG 知识库")
st.markdown("上传 Python 文档自动建库，或直接在下方提问")

# === 上传文件 ===
st.header("📁 上传文件")
uploaded = st.file_uploader("选择 .txt 或 .md 文件", type=["txt", "md"])

if uploaded is not None:
    with st.spinner("处理文件..."):
        text = uploaded.read().decode("utf-8", errors="ignore")
        
        # 切分成小块
        chunks = []
        chunk_size = 500
        overlap = 100
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - overlap
        
        st.write(f"切分为 {len(chunks)} 个片段")
        
        if st.button("✅ 添加到知识库"):
            embed_model = get_embed_model()
            docs = []
            ids = []
            for i, chunk in enumerate(chunks):
                docs.append(chunk)
                ids.append(f"uploaded_{uploaded.name}_{i}")
            
            st.session_state["db"].add(documents=docs, ids=ids)
            st.success(f"成功添加 {len(docs)} 个片段到知识库")

# === 对话区域 ===
st.header("💬 智能问答")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("问一个 Python 问题..."):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # 检索知识库
    with st.spinner("检索中..."):
        try:
            db = st.session_state["db"]
            q_emb = get_embedding(prompt)
            results = db.query(query_embeddings=[q_emb], n_results=3)
            contexts = results["documents"][0]
        except Exception as e:
            st.error(f"检索失败: {e}")
            contexts = []
    
    # 构造消息
    ctx = "\n\n".join(contexts)
    messages = [
        {"role": "system", "content": "你是Python编程助手。根据参考资料回答问题。"},
        {"role": "user", "content": f"参考资料：\n{ctx}\n\n问题：{prompt}"}
    ]
    
    # 调用千问
    with st.spinner("思考中..."):
        resp = client.chat.completions.create(model="qwen-plus", messages=messages)
    
    answer = resp.choices[0].message.content
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    
    with st.chat_message("assistant"):
        st.write(answer)

# === 页脚 ===
st.markdown("---")
st.caption("数据在 D:/SystemData/Python/damoxing/.vectorstore")
