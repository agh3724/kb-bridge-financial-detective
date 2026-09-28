import json

with open(r"c:\Users\user\Documents\One day project\kb-bridge-financial-detective\notebooks\analysis_anjihyeong.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

for i in range(min(11, len(nb['cells']))):
    cell = nb['cells'][i]
    print(f"\n{'='*20} CELL {i} [{cell['cell_type']}] {'='*20}")
    print("".join(cell.get('source', [])))
