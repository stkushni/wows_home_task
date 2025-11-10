# syntax=docker/dockerfile:1
FROM python:3.8-slim

ARG ALLURE_VERSION=2.27.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        unzip \
        openjdk-17-jre-headless \
        bash \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o /tmp/allure.zip \
        "https://github.com/allure-framework/allure2/releases/download/${ALLURE_VERSION}/allure-${ALLURE_VERSION}.zip" \
    && unzip /tmp/allure.zip -d /opt \
    && mv "/opt/allure-${ALLURE_VERSION}" /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/local/bin/allure \
    && rm /tmp/allure.zip

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["pytest", "-v", "--alluredir=/app/allure-results"]
