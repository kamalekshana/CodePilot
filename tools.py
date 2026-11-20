
from pathlib import Path
import subprocess
import sys


# Project directory
PROJECT_DIR = Path(__file__).parent.resolve()



def read_file(filename: str) -> str:
    """
    Safely read a text file inside the CodePilot project directory.
    """

    try:
        file_path = (PROJECT_DIR / filename).resolve()

        # Prevent access outside the project directory
        if not file_path.is_relative_to(PROJECT_DIR):
            return "Error: Access outside the project directory is not allowed."

        # Block sensitive files anywhere in the path
        if any(
            part.lower() in {".env", "secrets.toml"}
            or part.lower().startswith(".env.")
            for part in file_path.relative_to(PROJECT_DIR).parts
        ):
            return "Error: Access to sensitive configuration files is blocked."

        if not file_path.exists():
            return f"Error: File '{filename}' does not exist."

        if not file_path.is_file():
            return f"Error: '{filename}' is not a file."

        return file_path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        return "Error: This file is not a readable text file."

    except (OSError, ValueError, RuntimeError) as error:
        return f"Error reading file: {error}"



def create_file(filename: str, content: str) -> str:
    """
    Safely create a new file inside the CodePilot project directory.
    Validate Python syntax before creating Python files.
    """

    import ast

    try:
        file_path = (PROJECT_DIR / filename).resolve()

        # Prevent access outside the project directory
        if not file_path.is_relative_to(PROJECT_DIR):
            return "Error: Access outside the project directory is not allowed."

        # Block sensitive filenames and directories
        if any(
            part.lower() in {".env", "secrets.toml"}
            or part.lower().startswith(".env.")
            for part in file_path.relative_to(PROJECT_DIR).parts
        ):
            return "Error: Creating sensitive configuration files is blocked."

        if not isinstance(content, str):
            return "Error: File content must be text."

        # Validate syntax before creating Python files
        if file_path.suffix.lower() == ".py":
            try:
                ast.parse(content)
            except SyntaxError as error:
                return (
                    f"Error: Syntax error on line {error.lineno}: "
                    f"{error.msg}"
                )

        if file_path.exists():
            return f"Error: File '{filename}' already exists."

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        return f"Successfully created '{filename}'."

    except (OSError, ValueError, RuntimeError) as error:
        return f"Error creating file: {error}"



def run_python_file(filename: str, input_text: str = "") -> str:
    """
    Execute a Python file inside the CodePilot project directory.
    Supports predefined keyboard input for browser execution.
    """

    file_path = (PROJECT_DIR / filename).resolve()

    # Prevent execution of files outside the project
    if not file_path.is_relative_to(PROJECT_DIR):
        return "Error: Access outside the project directory is not allowed."

    if file_path.suffix.lower() != ".py":
        return "Error: Only Python files can be executed."

    if not file_path.exists() or not file_path.is_file():
        return f"Error: File '{filename}' does not exist."

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            cwd=str(PROJECT_DIR),
            input=input_text,
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout
        errors = result.stderr

        if result.returncode != 0:
            return (
                f"Program failed with exit code {result.returncode}.\n"
                f"Output:\n{output}\n"
                f"Errors:\n{errors}"
            )

        return output or "Program executed successfully with no output."

    except subprocess.TimeoutExpired:
        return "Error: Program exceeded the 10-second time limit."

    except OSError as error:
        return f"Execution error: {error}"

def run_python_file_interactive(filename: str) -> str:
    """
    Execute a Python file directly in the user's terminal.
    Allows the user to enter input while the program runs.
    """

    file_path = (PROJECT_DIR / filename).resolve()

    # Prevent access outside the project directory
    if not file_path.is_relative_to(PROJECT_DIR):
        return "Error: Access outside the project directory is not allowed."

    if file_path.suffix != ".py":
        return "Error: Only Python files can be executed."

    if not file_path.exists() or not file_path.is_file():
        return f"Error: File '{filename}' does not exist."

    try:
        print("\n========== INTERACTIVE EXECUTION ==========\n")

        result = subprocess.run(
            [sys.executable, str(file_path)],
            cwd=str(PROJECT_DIR)
        )

        if result.returncode == 0:
            return "Program finished successfully."

        return (
            f"Program exited with code {result.returncode}."
        )

    except OSError as error:
        return f"Execution error: {error}"

    except KeyboardInterrupt:
        return "Program execution interrupted by user."



def edit_file(filename: str, new_content: str) -> str:
    """
    Safely update an existing Python file inside the project directory.
    Validate syntax before writing changes.
    """

    import ast

    try:
        file_path = (PROJECT_DIR / filename).resolve()

        # Prevent access outside the project directory
        if not file_path.is_relative_to(PROJECT_DIR):
            return "Error: Access outside the project directory is not allowed."

        # Block sensitive filenames and directories
        if any(
            part.lower() in {".env", "secrets.toml"}
            or part.lower().startswith(".env.")
            for part in file_path.relative_to(PROJECT_DIR).parts
        ):
            return "Error: Editing sensitive configuration files is blocked."

        # Only allow editing Python files
        if file_path.suffix.lower() != ".py":
            return "Error: Only Python files can be edited."

        if not file_path.exists() or not file_path.is_file():
            return f"Error: File '{filename}' does not exist."

        if not isinstance(new_content, str):
            return "Error: File content must be text."

        # Validate syntax before modifying the file
        try:
            ast.parse(new_content)
        except SyntaxError as error:
            return (
                f"Error: Syntax error on line {error.lineno}: "
                f"{error.msg}"
            )

        file_path.write_text(new_content, encoding="utf-8")

        return f"Successfully updated '{filename}'."

    except (OSError, ValueError, RuntimeError) as error:
        return f"Error editing file: {error}"


if __name__ == "__main__":

    print("Testing CodePilot interactive execution...\n")

    result = run_python_file_interactive(
        "generated_program.py"
    )

    print("\n========== EXECUTION STATUS ==========\n")
    print(result)



def inspect_project() -> str:
    """
    List relevant files and folders inside the CodePilot project directory.
    Exclude development settings, temporary tests and sensitive files.
    """
    try:
        items = []

        ignored_directories = {
            ".venv",
            "__pycache__",
            ".git",
            ".vscode",
        }

        ignored_files = {
            ".env",
            "secrets.toml",
            "bug_test.py",
            "debug_test.py",
        }

        for path in sorted(PROJECT_DIR.rglob("*")):

            relative_path = path.relative_to(PROJECT_DIR)

            # Skip ignored directories and their contents
            if any(
                part.lower() in ignored_directories
                for part in relative_path.parts
            ):
                continue

            # Skip sensitive and temporary files
            if path.name.lower() in ignored_files:
                continue

            if path.name.lower().startswith(".env."):
                continue

            if path.is_file() and (
                path.name.lower().startswith("test_")
                or path.name.lower().endswith("_test.py")
            ):
                continue

            if path.is_file():
                items.append(f"FILE: {relative_path}")

            elif path.is_dir():
                items.append(f"FOLDER: {relative_path}")

        if not items:
            return "The project directory is empty."

        return "\n".join(items)

    except OSError as error:
        return f"Project inspection error: {error}"

def read_project_context(max_files: int = 10) -> str:
    """
    Read relevant Python and requirements files
    to provide context about the existing project.
    """
    context = []
    allowed_extensions = {".py", ".txt"}

    for path in sorted(PROJECT_DIR.rglob("*")):
        if (
            ".venv" in path.parts
            or "__pycache__" in path.parts
            or ".git" in path.parts
            or path.name in {".env", "secrets.toml"}
        ):
            continue

        if not path.is_file() or path.suffix not in allowed_extensions:
            continue

        if len(context) >= max_files:
            break

        relative_path = path.relative_to(PROJECT_DIR)

        content = read_file(str(relative_path))

        if content.startswith("Error:"):
            continue

        context.append(
            f"\n--- FILE: {relative_path} ---\n{content}"
        )

    if not context:
        return "No relevant project files found."

    return "\n".join(context)



def apply_file_changes(files: dict[str, str]) -> str:
    """
    Validate and create or update multiple Python files.
    """

    if not isinstance(files, dict) or not files:
        return "Error: No file changes were provided."

    validated_files = []

    # Validate every file before making changes.
    for filename, content in files.items():

        if not isinstance(filename, str) or not isinstance(content, str):
            return "Error: Invalid filename or file content."

        try:
            file_path = (PROJECT_DIR / filename).resolve()

            if not file_path.is_relative_to(PROJECT_DIR):
                return f"Error: Unsafe file path: {filename}"

            if any(
                part.lower() in {".env", "secrets.toml"}
                or part.lower().startswith(".env.")
                for part in file_path.relative_to(PROJECT_DIR).parts
            ):
                return "Error: Access to sensitive files is blocked."

            if file_path.suffix.lower() != ".py":
                return f"Error: Only Python files are supported: {filename}"

            # Validate Python syntax before saving.
            syntax_result = validate_python_code(content)

            if not syntax_result.startswith("Syntax validation successful"):
                return f"Error in {filename}: {syntax_result}"

            validated_files.append((filename, file_path, content))

        except (OSError, ValueError, RuntimeError) as error:
            return f"Error validating {filename}: {error}"

    # Save files only after every file passes validation.
    results = []

    for filename, file_path, content in validated_files:
        if file_path.exists():
            result = edit_file(filename, content)
        else:
            result = create_file(filename, content)

        results.append(result)

        if result.startswith("Error:"):
            return "\n".join(results)

    return "\n".join(results)

def validate_python_code(code: str) -> str:
    """
    Validate Python source code without executing it.
    """

    import ast

    try:
        ast.parse(code)
        return "Syntax validation successful."

    except SyntaxError as error:
        return (
            f"Syntax error on line {error.lineno}: "
            f"{error.msg}"
        )
