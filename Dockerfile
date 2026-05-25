FROM python:3.11-slim
WORKDIR /app
COPY external.txt .
RUN pip install -r external.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
