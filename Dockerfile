# syntax=docker/dockerfile:1
FROM python:3.12-slim-bullseye AS builder
WORKDIR /opt/talkback-slack-bot
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --without dev && \
    poetry build

FROM python:3.12-slim-bullseye
WORKDIR /opt/talkback-slack-bot
COPY --from=builder /opt/talkback-slack-bot/dist/*.whl /opt/talkback-slack-bot/dist/
COPY --from=builder /opt/talkback-slack-bot/pyproject.toml /opt/talkback-slack-bot/poetry.lock /opt/talkback-slack-bot/
ENV PYTHONPATH=/opt/talkback-slack-bot
RUN pip install dist/*.whl && \
    chmod -R 700 .
STOPSIGNAL SIGINT
ENTRYPOINT ["talkback-slack-bot"]