# syntax=docker/dockerfile:1
FROM python:3.12-slim-bullseye AS builder
WORKDIR /opt/talkback-messenger
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --without dev && \
    poetry build

FROM python:3.12-slim-bullseye
WORKDIR /opt/talkback-messenger
COPY --from=builder /opt/talkback-messenger/dist/*.whl /opt/talkback-messenger/dist/
COPY --from=builder /opt/talkback-messenger/pyproject.toml /opt/talkback-messenger/poetry.lock /opt/talkback-messenger/
ENV PYTHONPATH=/opt/talkback-messenger
RUN pip install dist/*.whl && \
    chmod -R 700 .
STOPSIGNAL SIGINT
ENTRYPOINT ["talkback-messenger"]