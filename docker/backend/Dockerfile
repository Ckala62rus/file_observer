FROM python:3.12-alpine

WORKDIR /src

COPY ./src/pyproject.toml \
    ./src/poetry.lock /src/

COPY ./src .

#RUN useradd -ms /bin/sh  eovchinnikov
#RUN adduser -D eovchinnikov www-data
#USER eovchinnikov

RUN apk --update add mc curl curl bash nano

RUN pip install poetry && pip install poetry-plugin-export && pip install tzdata

RUN apk --update add \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && pip install poetry \
    && poetry export --without-hashes -f requirements.txt --output requirements.txt \
    && pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt

# Create a group and user
RUN addgroup -S appgroup && adduser -S eovchinnikov -G appgroup
# Tell docker that all future commands should run as the appuser user
USER eovchinnikov

ENV TZ = Europe/Moscow

CMD ["timedatectl", "set-timezone", "Europe/Moscow"]
