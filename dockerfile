FROM python:3.7-slim AS base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS builder

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
COPY --from=builder /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN useradd --create-home app
WORKDIR /home/app
USER app

COPY . .
ENTRYPOINT ["python", "-m", "pyconsul"]
CMD ["-vv"]
