
# CodePilot — AI Coding Agent

CodePilot is a personal AI-powered coding agent built with Python and Streamlit.

It helps users generate Python programs, manage project files, execute code, identify errors, and apply AI-generated corrections.

## Features

- AI-powered Python code generation
- Single-file and multi-file project generation
- Project file explorer
- Python file creation and editing
- Code execution with predefined user input
- Execution output and error reporting
- Python syntax validation
- AI-powered error analysis and correction
- User approval before saving generated projects and applying corrections

## Technology Stack

- Python
- Streamlit
- OpenRouter API
- OpenAI Python SDK
- python-dotenv

## Project Structure

```text
aivar-project1/
├── agent.py
├── app.py
├── llm.py
├── tools.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Navigate into the project folder:

   ```bash
   cd aivar-project1
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it on Windows:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Create a `.env` file in the project directory:

   ```text
   OPENROUTER_API_KEY=your_api_key_here
   ```

7. Start CodePilot:

   ```bash
   streamlit run app.py
   ```

## Security

- API keys are stored in environment variables.
- The `.env` file is excluded from Git.
- File operations are restricted to the project directory.
- Generated code requires user approval before saving or execution.

Note: Project-directory restrictions are not a complete operating-system sandbox. Review generated code before running it.

## Project Status

Initial working prototype. Further testing and improvements are ongoing.

## Author

Developed as a college capstone project.
