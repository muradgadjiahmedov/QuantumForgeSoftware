# Задание 3 — Создание векторного индекса базы знаний

## Кратко
- **Модель эмбеддингов:** `BAAI/bge-base-en-v1.5` (768-мерные векторы) — https://huggingface.co/BAAI/bge-base-en-v1.5
- **Чанкинг:** `RecursiveCharacterTextSplitter` (LangChain), `chunk_size=800`, `chunk_overlap=150`.
- **Векторная БД:** FAISS (локально), путь сохранения: `./vector_store/faiss_index/`.
- **База знаний:** `./knowledge_base/` (результат Задания 2).

## Что входит
- `src/build_index.py` — создание индекса FAISS из `knowledge_base/`.
- `src/query_example.py` — пример поиска по индексу (similarity_search).
- `docs/INDEX_README.md` — шаблон отчёта о сборке индекса.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install langchain langchain-community sentence-transformers faiss-cpu python-dotenv
python src/build_index.py
python src/query_example.py --q "Как использовать Flux Compass для навигации?"
```
