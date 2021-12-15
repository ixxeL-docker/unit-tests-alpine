FROM alpine:latest AS builder

RUN apk update --no-cache \
    && apk add curl --no-cache --update \
    && curl -sLO "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64" \
    && chmod +x hadolint-Linux-x86_64 \
    && mv ./hadolint-Linux-x86_64 /usr/local/bin/hadolint \
    && curl -sL "https://github.com/stackrox/kube-linter/releases/latest/download/kube-linter-linux.tar.gz" | tar -xz \
    && chmod +x kube-linter \
    && mv ./kube-linter /usr/local/bin/kube-linter \
    && curl -sL "https://github.com/controlplaneio/kubesec/releases/latest/download/kubesec_linux_amd64.tar.gz" | tar -xz \
    && chmod +x kubesec \
    && mv ./kubesec /usr/local/bin/kubesec \
    && curl -sL "https://github.com/zegl/kube-score/releases/download/v1.13.0/kube-score_1.13.0_linux_amd64.tar.gz" | tar -xz \
    && chmod +x kube-score \
    && mv ./kube-score /usr/local/bin/kube-score

FROM alpine:latest

LABEL maintainer="Frederic Spiers <fredspiers@gmail.com>" \
      component="CI/CD tools"

ENV TZ="Europe/Paris" \
    IMG_VERSION="1.1.0"

COPY --from=builder /usr/local/bin/kube-score /usr/local/bin/kubesec /usr/local/bin/hadolint /usr/local/bin/kube-linter /usr/local/bin/

WORKDIR /usr/app

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && apk update --no-cache \
    && apk upgrade --no-cache \  
    && apk add --no-cache --update \
    curl \
    bash \
    jq \
    python3 \
    py3-pip \
    skopeo \
    shellcheck \
    black \
    nodejs \
    npm \
    tzdata \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime

RUN pip3 install --no-cache-dir flake8 flake8-json pytest pytest-cov coverage bandit

RUN npm install -g install-peerdeps \
                   jslint \
                   eslint \
                   jshint \
                   snyk@latest

RUN npx install-peerdeps -g eslint-config-airbnb \
    && npx install-peerdeps --dev eslint-config-airbnb-base \
    && npx install-peerdeps --dev eslint-config-standard \
    && npx install-peerdeps --dev eslint-config-prettier \
    && npx install-peerdeps --dev eslint-config-google
