with open(r'C:\Users\MuzaffarZed\.gemini\antigravity\brain\776c4a96-8eb4-4dda-9f36-a6e771149a78\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        if '"step_index":5396' in line:
            import json
            data = json.loads(line)
            print(data['tool_calls'][0]['args']['CommandLine'])
