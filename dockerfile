FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv pip install --system .

COPY . .

EXPOSE 8501

ENV PYTHONPATH=/app

CMD ["streamlit", "run", "app/dashboard.py", "--server.address=0.0.0.0"]