
FROM python:3.10

WORKDIR /usr/src/app

COPY ./Pipfile ./Pipfile.lock ./

RUN pip install pipenv && pipenv install --system --deploy

COPY slave .

CMD ["python", "-m", "slave:main"]