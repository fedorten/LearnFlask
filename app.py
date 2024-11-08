from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Правильная переменная конфигурации
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lernf.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/create', methods=['POST','GET'])
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

if __name__ == "__main__":
    app.run(debug=True)
