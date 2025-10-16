from .rag_bot import answer

def main():
    print("RAG REPL. Введите пустую строку для выхода.")
    while True:
        q = input("\nQ> ").strip()
        if not q:
            break
        ans, meta = answer(q)
        print("\nA>", ans)
        if meta:
            print("retrieved:", meta)

if __name__ == "__main__":
    main()
