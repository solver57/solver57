from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Список кортежей координат выделенных клеток
selected_cells = []

# Шаблон HTML для веб-страницы
@app.route("/data/<int:m>/<int:n>/")
def index(m, n):
    return render_template("index.html", m=m, n=n)

# Маршрут для обработки кликов по клеткам
@app.route("/click", methods=["POST"])
def click():
    x = int(request.form["x"])
    y = int(request.form["y"])
    cell = (x, y)
    if cell in selected_cells:
        selected_cells.remove(cell)
    else:
        selected_cells.append(cell)
    return jsonify({"selected_cells": selected_cells})

# Маршрут для обработки нажатия на кнопку
@app.route("/button", methods=["POST"])
def button():
    print(selected_cells)
    selected_cells.clear()
    return jsonify({"selected_cells": []})

if __name__ == "__main__":
    app.run(debug=True)
