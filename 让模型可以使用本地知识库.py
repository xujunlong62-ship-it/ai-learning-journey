import sys
import os
import json
import sqlite3

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from openai import OpenAI
from fastembed.embedding import TextEmbedding

load_dotenv(dotenv_path=r"D:\SystemData\Python\damoxing\.env", override=True)

# === 1. 连接 SQLite 对话记忆 ===
db_sqlite = sqlite3.connect("D:/SystemData/Python/damoxing/对话记忆/checkpoint.db", check_same_thread=False)
history = []

# === 2. 加载知识库 ===
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import numpy as np

embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path=r"D:\SystemData\Python\damoxing\.vectorstore")
db = client.get_collection(name="python_docs")

# === 3. 千问模型 ===
client_qwen = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("DASHSCOPE_BASE_URL"),
)

# === 4. 扩大检索 ===
def retrieve_chunks(question, top_k=10):
    """扩大检索：先查 10 个，后面再重排序"""
    q_emb = next(np.array(e, dtype=np.float32) for e in embed_model.embed([question])).tolist()
    results = db.query(query_embeddings=[q_emb], n_results=top_k)
    return results["documents"][0], results["distances"][0]

# === 5. 重排序：让千问挑最相关的 3 个 ===
def rerank_chunks(question, chunks):
    """把问题+10个片段发给千问，让它挑最相关的3个"""
    chunk_list = "\n---\n".join([f"[{i}] {c[:300]}" for i, c in enumerate(chunks)])
    resp = client_qwen.chat.completions.create(
        model="qwen-plus",
        messages=[
            {
                "role": "system",
                "content": "你是资料筛选助手。以下有10段Python文档片段。根据用户问题，选出最相关的3个。只返回3个数字，用逗号分隔，例如：2,5,8。不要返回其他内容。"
            },
            {"role": "user", "content": f"问题：{question}\n\n资料：\n{chunk_list}"}
        ]
    )
    selected = resp.choices[0].message.content.strip()
    indices = [int(x.strip()) for x in selected.split(",") if x.strip().isdigit()]
    # 确保在范围内
    indices = [i for i in indices if 0 <= i < len(chunks)]
    if not indices:
        indices = list(range(min(3, len(chunks))))
    return [chunks[i] for i in indices]

# === 6. 主函数：RAG + 对话记忆 ===
def rag_ask(question, top_k=10):
    global history
    
    # 扩大检索
    chunks, distances = retrieve_chunks(question, top_k=top_k)
    
    # 重排序：挑最相关的3个
    best_chunks = rerank_chunks(question, chunks)
    
    # 拼参考资料
    context = "\n\n".join(best_chunks)
    
    # 拼对话历史
    messages = [
        {"role": "system", "content": "你是一个Python编程助手。根据参考资料回答问题。"}
    ]
    # 加入历史
    for h in history:
        messages.append({"role": h["role"], "content": h["content"]})
    # 加入当前问题
    messages.append({"role": "user", "content": question})
    
    # 调用千问（带参考资料）
    messages.insert(1, {"role": "system", "content": f"参考资料：\n{context}\n\n规则：1.优先用参考资料回答 2.没有就说不知道 3.用中文回答"})
    
    resp = client_qwen.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=messages
    )
    answer = resp.choices[0].message.content
    
    # 保存对话历史
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    # 只保留最近5轮
    if len(history) > 10:
        history = history[-10:]
    
    print("=== 参考资料 ===")
    print(context[:500])
    print("\n=== 回答 ===")
    print(answer)
    return answer

print("知识库就绪，调用 rag_ask('问题') 即可")
print("\n=== 第一轮测试 ===")
rag_ask("Python 中如何处理 FileNotFoundError？")
print("\n\n=== 第二轮测试（追问） ===")
rag_ask("那 try except 怎么写？")
