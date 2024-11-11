from flask import Flask, render_template, request, redirect, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io
import base64
import os

# Инициализация Flask приложения
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lernf.db'  # Путь к базе данных
db = SQLAlchemy(app)

# Модели для базы данных
class Drawing(db.Model):
    __tablename__ = 'drawings'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

# Директория для сохранения изображений
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Маршруты для постов
@app.route('/')
def canvas():
    return render_template('canvas.html')

@app.route('/posts')
def posts():
    posts = Post.query.all()
    return render_template("posts.html", posts=posts)

@app.route('/img')
def img():
    # Получаем все изображения из базы данных
    drawings = Drawing.query.all()
    return render_template('img.html', drawings=drawings)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST': 
        title = request.form['title']
        text = request.form['text']

        post = Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()  # Откат транзакции в случае ошибки
            return f"ERROR 228: {e}"  # Выводим точную причину ошибки
        
    return render_template("create.html")

# Маршрут для сохранения изображений
@app.route("/save_drawing", methods=["POST"])
def save_drawing():
    data = request.get_json()
    image_data = data['image'].split(",")[1]  # Получаем только данные изображения
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))  # Декодируем изображение

    # Сохраняем изображение в файловой системе
    image_id = str(len(os.listdir(IMAGE_DIR)) + 1)  # Генерируем ID для нового изображения
    image_path = os.path.join(IMAGE_DIR, f"{image_id}.png")
    image.save(image_path)

    # Сохраняем путь к изображению в базе данных
    drawing = Drawing(image_path=image_path)
    db.session.add(drawing)
    db.session.commit()

    return jsonify({"image_id": drawing.id})

# Маршрут для просмотра изображений
@app.route("/view_drawing/<int:image_id>")
def view_drawing(image_id):
    drawing = Drawing.query.get(image_id)  # Запрашиваем рисунок по ID
    if drawing:
        return send_file(drawing.image_path, mimetype='image/png')
    else:
        return "Изображение не найдено", 404

if __name__ == "__main__":
    app.run(debug=True)
     # Создание таблиц при запуске
    with app.app_context():
        db.create_all()
    app.run(debug=True)
