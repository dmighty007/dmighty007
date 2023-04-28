# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Avinal Kumar <avinal.xlvii@gmail.com>
#
# Distributed under the terms of MIT License
# The full license is in the file LICENSE, distributed with this software.
FROM python:3.11.3-slim-bullseye
 
ENV PYTHONFAULTHANDLER=1 \
     PYTHONUNBUFFERED=1 \
     PYTHONHASHSEED=random \
     PYTHONDONTWRITEBYTECODE=1 \
     # pip:
     PIP_NO_CACHE_DIR=off \
     PIP_DISABLE_PIP_VERSION_CHECK=on \
     PIP_DEFAULT_TIMEOUT=100 \
     # poetry:
     POETRY_VERSION=2.0 \
     POETRY_NO_INTERACTION=1 \
     POETRY_CACHE_DIR='/var/cache/pypoetry' \
     PATH="$PATH:/root/.local/bin"
 
# install poetry
# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN apt-get update && apt-get install -y --no-install-recommends git && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*
RUN pip install pipx
RUN pipx install "poetry"
#RUN pipx install "poetry"
RUN pipx ensurepath 
# install dependencies
#COPY pyproject.toml poetry.lock /
ADD pyproject.toml /pyproject.toml
ADD requirements.txt /requirements.txt
RUN cat requirements.txt | grep -E '^[^# ]' | cut -d= -f1 | xargs -n 1 poetry add
RUN poetry install --no-dev --no-root --no-interaction --no-ansi
# Add files to docker
ADD main.py entrypoint.sh colors.json /

# run final script
#CMD python3 /main.py && /entrypoint.sh
RUN 
CMD [ "poetry", "run", "python", "/main.py" ]
CMD /entrypoint.sh