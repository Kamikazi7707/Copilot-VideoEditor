# Copilot-VideoEditor
# Video Editor Copilot Backend

A Flask-based AI assistant backend for video editing commands. Powered by OpenAI's GPT, it turns natural user prompts into editor actions and simulates “robot” steps.

---

## Project Structure

- `app.py` — Main Flask backend, with AI prompt understanding and action simulation.
- `requirements.txt` — All Python package dependencies (Flask, openai, etc.)

---

## Setup

1. **Clone this repository** (or copy the files into your workspace).
2. **Install the required Python packages:**
    ```
    pip install -r requirements.txt
    ```
3. **Set your OpenAI API key as an environment variable:**

    ```
    export OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxx
    ```

    - In GitHub Codespaces, [add your key as a Codespaces Secret](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces) for automatic loading.
    - Get your key at: https://platform.openai.com/account/api-keys

4. **Start the backend server:**
    ```
    python app.py
    ```

---

## Usage

Send a POST request to `/prompt` on the running server with your editing prompt.

**Example curl command:**
curl -X POST http://127.0.0.1:5000/prompt -H "Content-Type: application/json" -d '{"prompt":"remove the background noise"}

**Example server response:**
{"response":"Apply noise reduction filter.","robot":"Pretend: Apply noise reduction filter."}


You can replace `"remove the background noise"` with other editor commands, like:
- `"split scene"`
- `"fade in music"`
- `"add slow zoom"`

---

## OpenAI API Key

- Create an account at https://platform.openai.com/, and generate an API key in the [API Keys page](https://platform.openai.com/account/api-keys).
- For Codespaces, add your key as a secret named `OPENAI_API_KEY` in **Repository > Settings > Secrets and Variables > Codespaces**.

---

## Project Configuration

All major settings are in `app.py`.  
- Dependencies are in `requirements.txt`.
- The OpenAI API key is required for full “smart” prompt understanding.
- For now, the backend simulates editor actions for demonstration—future updates will include UI, “real robot” integration, and installers.

---

## Planned Features & Roadmap

- Frontend UI for prompt and response (browser or desktop app)
- Desktop-ready “robot” actioning (via PyAutoGUI or similar)
- Voice command integration
- Simple one-click install and update system for all users
- More advanced AI prompt chaining and action-mapping

---

## Contributing

Pull requests and feature requests are welcome! Please ensure new features are documented in this README and that dependencies are added to requirements.txt.

---

## License

MIT (or specify your own)

---

*Last updated: August 5 2025*
