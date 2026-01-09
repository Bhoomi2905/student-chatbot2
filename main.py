from flask import Flask, request, render_template
from openai import OpenAI
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = []

@app.route("/", methods=["GET","POST"])
def chat():
    global chat_history
    if request.method=="POST":
        q = request.form.get("question","").strip()
        if q:
            # Add user question
            chat_history.append(("You", q, datetime.now().strftime("%H:%M")))
            
            # Bot typing placeholder
            chat_history.append(("Bot", "<span class='typing'></span>", datetime.now().strftime("%H:%M")))
            
            # Call OpenAI GPT
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You are a helpful student assistant chatbot. Answer short in 1., 2., 3. points."},
                    {"role":"user","content":q}
                ]
            )
            answer = r.choices[0].message.content
            
            # Replace typing with actual answer
            chat_history[-1] = ("Bot", answer, datetime.now().strftime("%H:%M"))
            
    # Quick suggestions

    return render_template("index.html", chat_history=chat_history)

if __name__=="__main__":
    app.run(debug=True)