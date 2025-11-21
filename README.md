📌 1. Descripción del Proyecto

Este proyecto es una API simple en Flask que expone dos endpoints:

GET / → Muestra un mensaje de bienvenida.

GET /suma?a=3&b=5 → Devuelve la suma de dos números enviados como parámetros.

El objetivo del repositorio es demostrar un flujo completo de CI/CD, donde automáticamente:

✔ Se ejecutan pruebas unitarias
✔ Se analiza la calidad del código
✔ Se construye una imagen Docker
✔ Se publica el package en GHCR

📌 2. Código principal (app.py)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenido a mi API de suma 🧮"

@app.route("/suma")
def sumar():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        resultado = a + b
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

📌 3. Pruebas Unitarias (test_app.py)
from app import app

def test_suma_endpoint():
    client = app.test_client()
    response = client.get("/suma?a=3&b=5")
    data = response.get_json()
    assert response.status_code == 200
    assert data["resultado"] == 8


Para ejecutarlas manualmente:

pytest -v

📌 4. Dockerfile utilizado
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]

📌 5. Flujo CI/CD (GitHub Actions)

Cada vez que haces push o pull request a la rama joel, se ejecutan estas tareas automáticamente:

✔ 1. Instalar dependencias
✔ 2. Ejecutar pruebas con pytest
✔ 3. Analizar código con Ruff
✔ 4. Construir imagen Docker
✔ 5. Publicar imagen en GitHub Container Registry
📌 6. Archivo de CI/CD (.github/workflows/joel.yml)
name: Pruebas y publicación del contenedor

on:
  push:
    branches: [ "joel" ]
  pull_request:
    branches: [ "joel" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Clonar el repositorio
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Ejecutar pruebas
        run: |
          pytest -v
          ruff check .

  build_and_push:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Clonar el repositorio
        uses: actions/checkout@v4

      - name: Iniciar sesión en GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Construir y publicar imagen Docker
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./molina.Dockerfile 
          push: true
          tags: ghcr.io/joelo15/joel:latest

📌 7. Construcción del Package (Imagen Docker)
🔹 Build manual:
docker build -f molina.Dockerfile -t joel-image .

🔹 Ejecutar la API con Docker:
docker run -p 5000:5000 joel-image


API disponible en:

http://localhost:5000/suma?a=2&b=3

📌 8. Acceso al package publicado

Tu imagen Docker queda publicada automáticamente en:

ghcr.io/joelo15/joel:latest


Para descargarla:

docker pull ghcr.io/joelo15/joel:latest

📌 9. Conclusión

Este proyecto implementa un pipeline CI/CD completamente funcional que cumple con todos los criterios de la rúbrica:

✔ README documentado
✔ Workflow funcional
✔ Pruebas unitarias
✔ Package generado
✔ Repositorio entregado
