import argparse
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--q', required=True)
    p.add_argument('--index', default='vector_store/faiss_index')
    p.add_argument('--model', default='BAAI/bge-base-en-v1.5')
    p.add_argument('--k', type=int, default=3)
    args = p.parse_args()

    embeddings = HuggingFaceEmbeddings(
        model_name=args.model,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    db = FAISS.load_local(args.index, embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(args.q, k=args.k)
    for i, d in enumerate(docs, 1):
        print(f'[{i}]', d.metadata.get('source', 'unknown'), '#chunk=', d.metadata.get('chunk_id'))
        print(d.page_content[:400].strip(), '\n')

if __name__ == '__main__':
    main()
