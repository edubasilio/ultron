FROM basiliocode/python3-alpine3
RUN apk update && apk upgrade

RUN pip install --upgrade pip

#install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry self update
RUN poetry config virtualenvs.create false
#RUN poetry install --no-interaction --no-ansi

WORKDIR /app/ultron-web
COPY . /app/ultron-web
