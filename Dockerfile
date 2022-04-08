FROM python:3.8

WORKDIR /app
COPY . /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000", "--root-path=/study"]
CMD "inv start"