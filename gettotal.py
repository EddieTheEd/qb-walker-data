import json

with open(f'qb_science.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
print(len(data))
