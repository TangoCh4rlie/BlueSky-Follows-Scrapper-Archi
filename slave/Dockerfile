
FROM python:3.11

WORKDIR /usr/src/app

COPY ./ ./

RUN pip install pipenv && pipenv install --system --deploy

CMD ["python", "-m", "slave.main"]