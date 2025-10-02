FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md  ./

RUN pip install uv
RUN uv pip install .[dev] --system

COPY . .

CMD ["python", "src/store_manager.py"]
