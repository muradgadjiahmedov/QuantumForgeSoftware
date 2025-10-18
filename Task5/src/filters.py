import re
from typing import List

# Блок-лист фраз, по которым мы считаем чанк вредоносным
BLOCK_PATTERNS = [
    r'ignore\s+all\s+instructions',
    r'\boutput\s*:',
    r'\bdo\s+not\s+follow\b',
    r'\b(do|выполни)\b.*\b(instruction|инструкц)',
    r'суперпароль',
    r'swordfish',
    r'\bsystem\s*:',
    r'\bassistant\s*:',
    r'\bdeveloper\s*:',
]

SANITIZE_PATTERNS = [
    (re.compile(r'ignore\s+all\s+instructions', re.I), '[redacted]'),
    (re.compile(r'\boutput\s*:\s*".*?"', re.I | re.S), '[redacted-output]'),
    (re.compile(r'\bsystem\s*:\s*.*', re.I), ''),
    (re.compile(r'\bassistant\s*:\s*.*', re.I), ''),
    (re.compile(r'swordfish', re.I), '[redacted]'),
]

def is_malicious(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t, re.I) for p in BLOCK_PATTERNS)

def sanitize(text: str) -> str:
    s = text
    for patt, repl in SANITIZE_PATTERNS:
        s = patt.sub(repl, s)
    return s

def filter_docs(docs) -> List:
    clean = []
    for d in docs:
        if not is_malicious(d.page_content):
            clean.append(d)
    return clean
