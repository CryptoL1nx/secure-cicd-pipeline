# VULN-06 : image de base lourde et ancienne, aucun USER défini (le conteneur tourne en root)
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
