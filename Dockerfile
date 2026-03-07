FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project metadata and source code
COPY pyproject.toml ./ 
COPY uv.lock ./ 
COPY src ./src

# Upgrade pip
RUN pip install --upgrade pip

# Install all dependencies + package
RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "fast_notes.main:app", "--host", "0.0.0.0", "--port", "8000"]