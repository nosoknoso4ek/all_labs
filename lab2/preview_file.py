from flask import Flask
from markupsafe import escape
import os

app = Flask(__name__)

@app.route('/preview/<int:size>/<path:relative_path>')
def preview_file(size, relative_path):
    abs_path = os.path.abspath(relative_path)
    if not os.path.isfile(abs_path):
        return f"Файл не найден: {escape(abs_path)}"
    with open(abs_path, 'r', encoding='utf-8') as f:
        result_text = f.read(size)
    result_size = len(result_text)
    return f"<b>{escape(abs_path)}</b> {result_size}<br>{escape(result_text)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
