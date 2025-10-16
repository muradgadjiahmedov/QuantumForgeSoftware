import os, json, re

with open('knowledge_base/terms_map.json', 'r', encoding='utf-8') as f:
    TERMS = json.load(f)

def replace_terms(text: str) -> str:
    for old, new in sorted(TERMS.items(), key=lambda x: -len(x[0])):
        text = re.sub(r'\b' + re.escape(old) + r'\b', new, text)
    return text

os.makedirs('knowledge_base', exist_ok=True)

for name in os.listdir('raw_data'):
    src = os.path.join('raw_data', name)
    if not os.path.isfile(src):
        continue
    with open(src, 'r', encoding='utf-8') as f:
        t = f.read()
    t = replace_terms(t)
    with open(os.path.join('knowledge_base', name), 'w', encoding='utf-8') as f:
        f.write(t)

print('✅ Замена выполнена.')