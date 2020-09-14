FROM basiliocode/python3-alpine3
RUN apk update && apk upgrade

# install posgres client
RUN apk add --no-cache postgresql-dev postgresql-client

RUN pip install --upgrade pip

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry self update
RUN poetry config virtualenvs.create false

WORKDIR /app/ultron_web
COPY . /app/ultron_web

RUN poetry install --no-interaction --no-ansi
