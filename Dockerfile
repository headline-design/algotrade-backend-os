FROM tiangolo/uvicorn-gunicorn:python3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /app/app
COPY ./app /app/app
ENV PYTHONPATH=/app
