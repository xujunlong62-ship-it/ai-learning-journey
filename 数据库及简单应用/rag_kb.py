import os
import chromadb
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# === 1. 加载文档 ===
loader = DirectoryLoader(
    'D:\\知识库',
    glob='**/*.md',
    loader_cls=lambda path: TextLoader(str(path), encoding='utf-8'),
    show_progress=True
)
documents = loader.load()
print(f'加载了 {len(documents)} 个文档')

# === 2. 文本切分 ===
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=['\n\n', '\n', '。', '.', ' ']
)
chunks = text_splitter.split_documents(documents)
print(f'切分为 {len(chunks)} 个文本块')

# === 3. 用 fastembed 做嵌入 ===
from fastembed.embedding import TextEmbedding

embed_model = TextEmbedding(model_name='BAAI/bge-small-en-v1.5')

class ChromaFastEmbed:
    def __init__(self, model):
        self.model = model
        self._name = 'bge-small-en-v1.5'
    
    def name(self):
        return self._name
    
    def __call__(self, input):
        return list(self.model.embed(input))

embed_func = ChromaFastEmbed(embed_model)

# === 4. 存入 Chroma ===
db_path = 'D:\\SystemData\\Python\\damoxing\\.vectorstore'
client = chromadb.PersistentClient(path=db_path)
db = client.get_or_create_collection(
    name='python_docs',
    embedding_function=embed_func
)
db.add(
    documents=[doc.page_content for doc in chunks],
    ids=[f'chunk_{i}' for i in range(len(chunks))]
)
print(f'知识库已保存到: {db_path}')
print(f'共 {db.count()} 条向量')
