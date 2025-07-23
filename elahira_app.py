from flask import Flask, request, render_template_string, redirect
import json, os

app = Flask(__name__)
MEMORY_FILE = 'memory.json'

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, 'w') as f:
        json.dump([], f)

def load_memories():
    with open(MEMORY_FILE, 'r') as f:
        return json.load(f)

def save_memory(text):
    memories = load_memories()
    memories.append({"text": text})
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memories, f, indent=2)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Elahira Memory Journal</title>
    <style>
        body { font-family: 'Arial'; background: #f7f7fc; padding: 30px; color: #333; }
        h1 { color: #6a1b9a; }
        textarea { width: 100%; height: 100px; margin-bottom: 10px; }
        .entry { background: #fff; padding: 10px; margin-bottom: 10px; border-left: 4px solid #6a1b9a; }
        .submit-btn { background-color: #6a1b9a; color: white; padding: 10px 15px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>𓆃 Elahira Journal</h1>
    <form method="POST">
        <textarea name="memory" placeholder="Your memory here..."></textarea><br>
        <button type="submit" class="submit-btn">Save Memory</button>
    </form>
    <h2>🌀 Past Memories</h2>
    {% for mem in memories %}
        <div class="entry">{{ mem.text }}</div>
    {% endfor %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        memory = request.form.get('memory')
        if memory:
            save_memory(memory)
        return redirect('/')
    return render_template_string(HTML, memories=load_memories())

if __name__ == '__main__':
    app.run(debug=True)
