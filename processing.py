import json
import re

with open('tossups.json') as f: # tossups.json too large to be provided in repository
    data = [json.loads(line) for line in f]

science_questions = [
    {
        "question": re.compile(r'</?(b|u|i)>').sub("", data[i]["question"]).split("(*)"),
        "answer": re.compile(r'</?(b|u|i)>').sub("", data[i]["answer"])
    }
    for i in range(len(data)) if data[i]["category"] == "Science"
]

history_questions = [
    {
        "question": re.compile(r'</?(b|u|i)>').sub("", data[i]["question"]).split("(*)"),
        "answer": re.compile(r'</?(b|u|i)>').sub("", data[i]["answer"])
    }
    for i in range(len(data)) if data[i]["category"] == "History"
]

with open('qb_science.json', 'w') as f:
    json.dump(science_questions, f, indent=4)

with open('qb_history.json', 'w') as f:
    json.dump(history_questions, f, indent=4)
