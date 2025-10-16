# Задание 4 — RAG-бот с few-shot и безопасным CoT

Этот пакет поднимает минимальный RAG-пайплайн поверх индекса FAISS (из задания 3) и добавляет:
- **Few-shot prompting** — 2 примера в той же предметной области.
- **Безопасный CoT** — модель размышляет скрытно и выдаёт только краткий ответ + ссылки на источники.  
  > Мы умышленно **не просим модель печатать пошаговые рассуждения**, чтобы не раскрывать chain-of-thought. Вместо этого она даёт короткое объяснение (до 2 предложений) и ссылки на чанки.

## Что внутри
- `src/rag_bot.py` — модуль с пайплайном (загрузка индекса, ретрив, промптинг, ответ).
- `src/serve.py` — FastAPI endpoint (`/ask`).
- `src/cli.py` — простой консольный REPL.
- `docs/EXAMPLES.md` — 3–5 успешных диалогов + 2 случая «Я не знаю».
- `.env.example` — переменные окружения для LLM (OpenAI).

## Быстрый старт
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# Помести свой индекс из Задания 3 в ./vector_store/faiss_index/
# либо собери новый (см. задание 3)

# Консольный режим
python src/cli.py

# API-режим
uvicorn src.serve:app --host 0.0.0.0 --port 8000 --reload
# POST http://localhost:8000/ask  { "query": "Как работает Synth Flux?" }
```

## LLM
По умолчанию используется OpenAI через `langchain-openai` (модель `gpt-4o-mini`), задайте `OPENAI_API_KEY` в `.env`.  
Можно заменить на любую поддерживаемую LangChain LLM — достаточно адаптировать `get_llm()` в `rag_bot.py`.

## Отказ от ответа
Если релевантность низкая (порог по score) — бот отвечает: **«Я не знаю»**.