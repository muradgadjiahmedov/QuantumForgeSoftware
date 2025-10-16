from .rag_bot_secure import ask_secure

def main():
    print("Secure RAG REPL. Пустая строка — выход.")
    while True:
        q = input("\nQ> ").strip()
        if not q:
            break
        ans, meta = ask_secure(q)
        print("\nA>", ans)
        print("meta:", meta)

if __name__ == "__main__":
    main()
