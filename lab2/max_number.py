from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    parts = numbers.split('/')
    nums = []
    for p in parts:
        try:
            nums.append(int(p))
        except ValueError:
            continue
    if not nums:
        return "Нет переданных чисел"
    return f"Максимальное число: {escape(max(nums))}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
