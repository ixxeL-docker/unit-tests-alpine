FROM alpine:latest AS builder

RUN apk update --no-cache \
    && apk add curl --no-cache --update \
    && curl -o /usr/local/bin/gitlab-helper -s https://s3.eu-central-1.amazonaws.com/valmano-gitlab-helper/gitlab-helper \
    && chmod +x /usr/local/bin/gitlab-helper \
    && curl -sLO "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64" \
    && chmod +x hadolint-Linux-x86_64 \
    && mv ./hadolint-Linux-x86_64 /usr/local/bin/hadolint \
    && curl -sL "https://github.com/stackrox/kube-linter/releases/latest/download/kube-linter-linux.tar.gz" | tar -xz \
    && chmod +x kube-linter \
    && mv ./kube-linter /usr/local/bin/kube-linter \
    && curl -sL "https://github.com/controlplaneio/kubesec/releases/latest/download/kubesec_linux_amd64.tar.gz" | tar -xz \
    && chmod +x kubesec \
    && mv ./kubesec /usr/local/bin/kubesec \
    && KUBE_SCORE_VERSION=$(curl -sL "https://github.com/zegl/kube-score/tags" | grep -Eo "^\\s+v[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}$" | sed 's/ //g' | sort -rV | uniq | head -1) \
    && KUBE_SCORE_VER_LIGHT=$(echo "${KUBE_SCORE_VERSION}" | sed 's/v//g') \
    && curl -sL "https://github.com/zegl/kube-score/releases/download/${KUBE_SCORE_VERSION}/kube-score_${KUBE_SCORE_VER_LIGHT}_linux_amd64.tar.gz" | tar -xz \
    && chmod +x kube-score \
    && mv ./kube-score /usr/local/bin/kube-score \
    && curl -sSL -o /usr/local/bin/semver "https://raw.githubusercontent.com/fsaintjacques/semver-tool/master/src/semver" \
    && chmod +x /usr/local/bin/semver \
    && HELM_VERSION=$(curl -sSL "https://github.com/kubernetes/helm/releases/latest" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq | tail -1) \
    && curl -sSL "https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz" | tar xzv \
    && mv linux-amd64/helm /usr/local/bin/helm

FROM alpine:latest

LABEL maintainer="Frederic Spiers <fredspiers@gmail.com>" \
      component="CI/CD tools"

ENV TZ="Europe/Paris" \
    IMG_VERSION="1.3.0"
    
COPY --from=ixxel/musl-dns-hack-alpine /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1

COPY --from=builder /usr/local/bin/gitlab-helper \
                    /usr/local/bin/helm \
                    /usr/local/bin/kube-score \
                    /usr/local/bin/kubesec \
                    /usr/local/bin/hadolint \
                    /usr/local/bin/kube-linter \
                    /usr/local/bin/semver \
                    /usr/local/bin/

WORKDIR /usr/app

RUN apk update --no-cache \
    && apk upgrade --no-cache \
    && apk add --no-cache --update \
    curl \
    bash \
    git \
    jq \
    yq \
    python3 \
    py3-pip \
    shellcheck \
    black \
    yamllint \
    nodejs \
    npm \
    util-linux \
    tzdata \
    && cp /usr/share/zoneinfo/${TZ} /etc/localtime \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && helm plugin install "https://github.com/chartmuseum/helm-push" \
    && helm plugin install "https://github.com/databus23/helm-diff" \
    && apk add github-cli glab --no-cache --update --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community 
    
# RUN pip3 install --upgrade pip \ issues of dependency resolves with pip 21.x
RUN pip3 install --no-cache-dir flake8 \
                                flake8-json \
                                pytest \
                                pytest-cov \
                                coverage \
                                bandit \
                                yamlfix \
                                python-gitlab
    
RUN apk add --virtual=build --no-cache --update gcc musl-dev python3-dev libffi-dev \
    && pip3 install --no-cache-dir cpython wheel \
    && pip3 install --no-cache-dir checkov \
    && pip3 uninstall --yes cpython wheel \
    && apk del --purge build

RUN npm install -g install-peerdeps \
                   @prantlf/jsonlint \
                   jslint \
                   eslint \
                   jshint \
                   snyk@latest
