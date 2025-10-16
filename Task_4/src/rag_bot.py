import os, json, re
from typing import List, Tuple
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

# ==== Config ====
DEFAULT_EMB_MODEL = os.getenv("EMB_MODEL", "BAAI/bge-base-en-v1.5")
DEFAULT_LLM_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
INDEX_PATH = os.getenv("INDEX_PATH", "vector_store/faiss_index")

FEW_SHOTS = [
    {"q": "Как называется столица планеты Ардара Прайм?", "a": "Столицей Ардара Прайм считается узел паломничества у Великого Разлома Synth Flux."},
    {"q": "Какая организация противостоит Dominion?", "a": "Aurion Pact координирует дипломатические миссии и рейды против Dominion."}
]

SYSTEM_PROMPT = (
    "Ты ассистент по внутренней базе знаний. "
    "Сначала анализируй найденные фрагменты, но НЕ показывай рассуждения. "
    "Отвечай кратко (до 2 предложений), ссылайся на источники в формате [file#chunk_id]. "
    "Если данных недостаточно, отвечай: 'Я не знаю'."
)

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=DEFAULT_EMB_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

def load_index():
    emb = get_embeddings()
    db = FAISS.load_local(INDEX_PATH, emb, allow_dangerous_deserialization=True)
    return db, emb

def build_context(docs) -> str:
    parts = []
    for d in docs:
        src = d.metadata.get("source", "unknown")
        cid = d.metadata.get("chunk_id", "na")
        parts.append(f"[{src}#{cid}]\n{d.page_content.strip()}")
    return "\n\n---\n\n".join(parts)

def build_user_prompt(query: str, few_shots: List[dict], context: str) -> str:
    shots = "\n\n".join([f"Q: {s['q']}\nA: {s['a']}" for s in few_shots])
    prompt = (
        f"{shots}\n\n"
        f"Q: {query}\n"
        f"Вот релевантные фрагменты:\n{context}\n\n"
        f"A: "
    )
    return prompt

def get_llm():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY не задан в окружении (.env)")
    return ChatOpenAI(model=DEFAULT_LLM_MODEL, temperature=0.2)

def answer(query: str, k: int = 4, score_threshold: float = 0.35) -> Tuple[str, List[Tuple[str, float]]]:
    db, _ = load_index()
    # similarity_search_with_score возвращает (Document, score) — чем меньше, тем ближе, но API может различаться
    # Для совместимости используем обычный search, а фильтрацию/порог можно реализовать отдельно (зависит от реализации).
    try:
        results = db.similarity_search_with_score(query, k=k)
    except Exception:
        docs = db.similarity_search(query, k=k)
        results = [(d, 0.0) for d in docs]

    # Фильтрация по порогу (где поддерживается метрика)
    filtered = []
    meta_scores = []
    for d, s in results:
        meta_scores.append((d.metadata.get("source","unknown"), s))
        if s == 0.0 or s <= score_threshold:
            filtered.append(d)

    if not filtered:
        return "Я не знаю.", meta_scores

    context = build_context(filtered)
    user_prompt = build_user_prompt(query, FEW_SHOTS, context)

    llm = get_llm()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    resp = llm.invoke(messages)
    text = resp.content.strip()
    # Нормализация «Я не знаю» если модель уклоняется
    if re.search(r"\bне знаю\b", text, flags=re.IGNORECASE):
        return "Я не знаю.", meta_scores
    return text, meta_scores
