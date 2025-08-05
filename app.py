import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def root():
    return jsonify({"message": "Server running. Use /prompt endpoint."})

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.get_json()
    user_prompt = data.get('prompt', '').lower()
    action = ""
    robot_done = ""

    # Always try OpenAI call first
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert video editing assistant. Translate user commands into short, clear video editor actions (like 'Splitting the video.')"},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=24,
            temperature=0
        )
        action = completion.choices[0].message.content.strip()
        robot_done = f"Pretend: {action}"
        print(robot_done)
        return jsonify({'response': action, 'robot': robot_done})
    except Exception as e:
        print(f"OpenAI Error: {e}")
        # FALLBACK: simple command matching below

    if "split" in user_prompt:
        action = "Splitting the video."
        robot_done = "Pretend: Pressing shortcut to split."
        print(robot_done)
    elif "fade" in user_prompt:
        action = "Adding a fade effect."
        robot_done = "Pretend: Moving mouse to apply fade."
        print(robot_done)
    elif "zoom" in user_prompt:
        action = "Applying slow zoom."
        robot_done = "Pretend: Clicking on zoom controls."
        print(robot_done)
    else:
        action = "Sorry, I don't know that command yet."
        robot_done = ""
    return jsonify({'response': action, 'robot': robot_done})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

