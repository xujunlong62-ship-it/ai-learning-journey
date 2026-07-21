import sys
import chromadb
import numpy as np
from fastembed.embedding import TextEmbedding
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv(dotenv_path=r"D:\SystemData\Python\damoxing\.env", override=True)

model = init_chat_model(
    model="qwen3.5-omni-plus",
    model_provider="openai",
    base_url=os.getenv("dashscope_base_url"),
    api_key=os.getenv("dashscope_api_key"),
)
agent = create_agent(model=model)

embed_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
db = chromadb.PersistentClient(path=r"D:\SystemData\Python\damoxing\.vectorstore").get_collection(
    name="python_docs"
)

def rag_ask(question, top_k=3):
    q_emb = embed_model.embed([question])
    q_emb = next(np.array(e, dtype=np.float32) for e in q_emb).tolist()
    ctx = "\n\n".join(db.query(query_embeddings=[q_emb], n_results=top_k)["documents"][0])
    resp = agent.invoke({"messages": [
        SystemMessage(content=f"""你是一个Python编程助手。
## 参考资料
{ctx}
## 规则
1. 优先用参考资料回答，没有就说不知道
2. 用中文回答，代码用 Python 格式"""),
        HumanMessage(content=question),
    ]})
    ans = next((m.content for m in resp.get("messages", []) if isinstance(m, AIMessage)), "")
    print(ans)
    return ans

print(rag_ask("Python 中如何处理 FileNotFoundError？"))
