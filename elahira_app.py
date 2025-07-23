from flask import Flask, render_template, request, redirect, url_for, session
import openai
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "elahira-secret"
openai.api_key = os.getenv("OPENAI_API_KEY")

memory_log = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        entry = request.form["entry"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        memory_log.append({"entry": entry, "timestamp": timestamp})

        # Optional GPT-4o memory reflection
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You're a memory reflection assistant."},
                    {"role": "user", "content": f"Reflect on this: {entry}"}
                ]
            )
            reflection = response.choices[0].message["content"]
        except:
            reflection = "Memory saved."

        return render_template("index.html", memory_log=memory_log, reflection=reflection)
    
    return render_template("index.html", memory_log=memory_log)

if __name__ == "__main__":
    app.run(debug=True)
