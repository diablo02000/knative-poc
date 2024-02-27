FROM python:3-slim AS base

ARG cnb_uid=1000
ARG cnb_gid=1000
ARG cnb_stack_id="python3-ffmpeg"

ENV CNB_USER_ID=${cnb_uid}
ENV CNB_GROUP_ID=${cnb_gid}
ENV CNB_STACK_ID=${cnb_stack_id}

# Set required CNB target information
LABEL io.buildpacks.base.distro.name="Debian"
LABEL io.buildpacks.base.distro.version="Slim Bookworm"
LABEL io.buildpacks.stack.id="${cnb_stack_id}"

# Create user and group
RUN groupadd cnb --gid ${cnb_gid} && \
  useradd --uid ${cnb_uid} --gid ${cnb_gid} -m -s /bin/bash cnb

RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6 libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/cache/*

FROM base AS build

RUN apt-get update && apt-get install -y build-essential zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/cache/*

# Set user and group
USER ${cnb_uid}:${cnb_gid}

FROM base as run

# Set user and group
USER ${cnb_uid}:${cnb_gid}
