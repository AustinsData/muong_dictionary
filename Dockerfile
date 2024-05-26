FROM python:3.10

WORKDIR /muongdict-app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./src ./src

COPY ./src/app/data/data.csv ./data/data.csv

COPY ./src/app/data/progress_data.csv ./data/progress_data.csv

EXPOSE 8080

CMD ["python", "./src/app/app.py"]