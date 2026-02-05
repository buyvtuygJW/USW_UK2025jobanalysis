FROM python:3.11-slim
WORKDIR /app
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt --ignore-requires-python || true
COPY . .
ENV PORT=8080
CMD ["streamlit", "run", "appv1.py", "--server.port=8080", "--server.address=0.0.0.0"]


