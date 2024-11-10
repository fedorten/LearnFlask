let canvas, ctx;
let drawing = false;
let shapeColor = "#808080"; 

window.onload = function() {
    canvas = document.getElementById("drawingCanvas");
    ctx = canvas.getContext("2d");

    // Добавление обработчиков событий для рисования
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseleave", stopDrawing);
};

// Начало рисования
function startDrawing(event) {
    drawing = true;
    draw(event); // Запуск рисования
}

// Остановка рисования
function stopDrawing() {
    drawing = false;
    ctx.beginPath(); // Прекращаем путь
}

// Рисование на холсте
function draw(event) {
    if (!drawing) return;
    ctx.strokeStyle = shapeColor;
    ctx.lineWidth = 2;
    ctx.lineCap = "round";
    
    // Координаты относительно холста
    const x = event.clientX - canvas.offsetLeft;
    const y = event.clientY - canvas.offsetTop;
    
    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Генерация случайной фигуры
function generateShape() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const shapeType = ["circle", "square", "triangle"][Math.floor(Math.random() * 3)];
    ctx.strokeStyle = shapeColor;
    ctx.beginPath();
    if (shapeType === "circle") {
        ctx.arc(250, 250, 50, 0, Math.PI * 2);
    } else if (shapeType === "square") {
        ctx.rect(200, 200, 100, 100);
    } else if (shapeType === "triangle") {
        ctx.moveTo(250, 200);
        ctx.lineTo(200, 300);
        ctx.lineTo(300, 300);
        ctx.closePath();
    }
    ctx.stroke();
    ctx.beginPath();
}



// Отправка рисунка на сервер
function submitDrawing() {
    const dataURL = canvas.toDataURL();
    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ drawing: dataURL })
    }).then(response => response.json()).then(data => {
        alert("Оригинальность: " + data.originality_score + "%");
        
        // Очищаем холст после отправки
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Генерируем новую фигуру
        generateShape();
    });

}
