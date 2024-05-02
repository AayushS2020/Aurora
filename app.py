from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

def run_python_file(input_text):
    text_file_paths = [
        "inputfileerror.txt",
        "inputfilegen.txt",
        "inputfilecontent.txt",
        "inputfilesummary.txt",
        "inputresearch.txt"
    ]
    python_file_paths = [
        "python_files/code_error.py",
        "python_files/code_gen.py",
        "python_files/content_gen.py",
        "python_files/content_summary.py",
        "python_files/research.py"
    ]

    for text_file_path, python_module_path in zip(text_file_paths, python_file_paths):
        with open(text_file_path, "r") as file:
            text_file_contents = file.read().strip().lower()

        if input_text.strip().lower() == text_file_contents:
            module_spec = importlib.util.find_spec(python_module_path)
            if module_spec:
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                if hasattr(module, "main") and callable(module.main):
                    return module.main(input_text)
                else:
                    return "Python file does not contain a main function."
            else:
                return "Python file not found."

    return "No matching text found."

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            output = run_python_file(user_input)
    return render_template("index.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)