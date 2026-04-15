import json

input_file = "/Users/samuel.salcedo/Samuel Salcedo/IA_Big_Data/Voz-propia/VoxPropia/modelo/planLector/dataset_finetune.jsonl"
output_file = "/Users/samuel.salcedo/Samuel Salcedo/IA_Big_Data/Voz-propia/VoxPropia/modelo/planLector/dataset_finetune.json"

all_pairs = []

with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            all_pairs.append(json.loads(line))

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_pairs, f, ensure_ascii=False, indent=4)

print(f"Successfully converted {len(all_pairs)} entries to a single JSON array at {output_file}")
