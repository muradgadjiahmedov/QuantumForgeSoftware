import os, time, json, argparse, pathlib
from typing import List
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings  # альтернатива (облако)

def load_documents(kb_dir: str):
    exts = {'.md', '.txt'}
    docs = []
    for root, _, files in os.walk(kb_dir):
        for name in files:
            if pathlib.Path(name).suffix.lower() in exts:
                path = os.path.join(root, name)
                loader = TextLoader(path, encoding='utf-8')
                docs.extend(loader.load())
    return docs

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('--kb', default='knowledge_base')
    parser.add_argument('--out', default='vector_store/faiss_index')
    parser.add_argument('--model', default='BAAI/bge-base-en-v1.5')
    parser.add_argument('--chunk_size', type=int, default=800)
    parser.add_argument('--chunk_overlap', type=int, default=150)
    args = parser.parse_args()

    t0 = time.time()
    print(f'[i] Загрузка из {args.kb} ...')
    docs = load_documents(args.kb)
    print(f'[i] Файлов: {len(docs)}')

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size, chunk_overlap=args.chunk_overlap,
        separators=['\n\n', '\n', '. ', '.', ' ']
    )
    chunks = splitter.split_documents(docs)
    for i, d in enumerate(chunks):
        d.metadata['chunk_id'] = i
    print(f'[i] Чанков: {len(chunks)}')

    print(f'[i] Эмбеддинги: {args.model} (dim=768)')
    embeddings = HuggingFaceEmbeddings(
        model_name=args.model,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    # embeddings = OpenAIEmbeddings(model='text-embedding-3-small')  # 1536 dim

    print('[i] Создание индекса FAISS ...')
    db = FAISS.from_documents(chunks, embeddings)
    os.makedirs(args.out, exist_ok=True)
    db.save_local(args.out)
    print(f'[✓] Сохранено в {args.out}; время: {time.time()-t0:.1f}s')

if __name__ == '__main__':
    main()
