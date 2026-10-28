# AWS Amplify build image for this site (see amplify.yml), pushed to ECR Public
# by .github/workflows/build-image.yml. Amplify requires curl, git, OpenSSH,
# bash, and Node + npm; the ruby image's buildpack-deps base supplies all but
# Node.
ARG RUBY_VERSION

FROM public.ecr.aws/docker/library/node:24-bookworm AS node
FROM ghcr.io/astral-sh/uv:0.13.5 AS uv

FROM public.ecr.aws/docker/library/ruby:${RUBY_VERSION}-bookworm

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s ../lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s ../lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx \
    && ln -s ../lib/node_modules/corepack/dist/corepack.js /usr/local/bin/corepack \
    && corepack enable
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0

COPY --from=uv /uv /uvx /usr/local/bin/
