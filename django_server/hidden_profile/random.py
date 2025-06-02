import json
import ast
s='{\n  "summarization": {"score": 10, "justification": "Only a single line with no substantial discussion or multiple points."},\n  "nudging": {"score": 10, "justification": "Insufficient context; multiple participants or their engagement levels aren\'t clear."},\n  "devils_advocate": {"score": 10, "justification": "No agreement or proposals present to challenge; too early to apply."}\n}'
s=json.loads(s)

print(type(s))