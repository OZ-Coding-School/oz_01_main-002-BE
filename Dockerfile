FROM python:3.12
LABEL maintainer='Samiiz'

ENV PYTHONUNBUFFERED 1

# mv랑 비슷함
COPY ./poetry.lock app/poetry.lock
COPY ./pyproject.toml app/pyproject.toml
COPY ./app /app/app
COPY ./scripts/run.sh /app/scripts/run.sh
COPY ./main.py /app
COPY ./README.md /app

# 작업시 /app 이 자동으로 붙는다
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m pip install --upgrade pip && \
    python -m pip install poetry && \
    poetry config virtualenvs.create true && \
    poetry config virtualenvs.in-project true && \
    if [ "$DEV" = "true" ]; \
        then echo "===THIS IS DEVELOPMENT BUILD===" && \
        poetry install --with dev ; \
    fi && \
    poetry install --without dev && \
    mkdir -p /vol/web && \
    chmod -R 755 /vol/web && \
    chmod -R +x /app/scripts && \
    chmod -R 777 /app/app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

USER root

CMD ["sh", "scripts/run.sh"]