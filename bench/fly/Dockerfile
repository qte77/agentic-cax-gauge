# Throwaway sandbox for benchmark runs (plan §5 BENCH-2). Model-written scripts execute here,
# never in the Codespace (bwrap has no user namespaces there). Built by Fly's remote builder
# from the repo root: see bench/fly/README.md. No ports, no services.
#
# Tags are pinned to a version; Dependabot (docker ecosystem, /bench/fly) bumps them.
FROM ghcr.io/astral-sh/uv:0.12.5 AS uv

FROM node:22-bookworm-slim
COPY --from=uv /uv /uvx /usr/local/bin/
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# OpenSCAD for that track; curl + certificates for the SolidCraft download. Versions are
# the bookworm ones resolved on 2026-10-26; a security update that drops one from the
# archive fails the build loudly — bump it here.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openscad=2021.01-6 ca-certificates=20250419~deb12u2 curl=7.88.1-10+deb12u15 \
    && rm -rf /var/lib/apt/lists/*

# SolidCraft CLI, release v0.23.1, checksum from the release's own SHA256SUMS.txt.
ARG SOLIDCRAFT_VERSION=0.23.1
ARG SOLIDCRAFT_SHA256=9db7de21f47000d0243ca361f6bf69f8652e7904da1b58e5f8c6f97c8dc69a13
RUN curl -fsSL -o /tmp/sc.tgz \
        "https://github.com/tangency-labs/solidcraft/releases/download/v${SOLIDCRAFT_VERSION}/solidcraft-${SOLIDCRAFT_VERSION}-linux-x86_64.tar.gz" \
    && echo "${SOLIDCRAFT_SHA256}  /tmp/sc.tgz" | sha256sum -c - \
    && tar -xzf /tmp/sc.tgz -C /opt \
    && ln -s "/opt/solidcraft-${SOLIDCRAFT_VERSION}-linux-x86_64/bin/solidcraft-cli" /usr/local/bin/solidcraft-cli \
    && rm /tmp/sc.tgz

# Claude Code, exact version (the npm package needs Node 22+, hence the base image).
ARG CLAUDE_CODE_VERSION=2.1.310
RUN npm install -g "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}" && npm cache clean --force

RUN useradd --create-home --shell /bin/bash bench
USER bench
ENV UV_CACHE_DIR=/home/bench/.cache/uv \
    UV_PYTHON_INSTALL_DIR=/home/bench/.python \
    DISABLE_AUTOUPDATER=1
WORKDIR /home/bench/app
COPY --chown=bench:bench . .
# Warm the tool caches one layer each: a single ~1 GB layer failed to push twice
# ("error rendering push status stream: unexpected EOF").
# With dev deps: `uv run` syncs the default groups, so a --no-dev env is re-synced on first use.
RUN uv sync --frozen
RUN uv run --no-project --with build123d python -c "import build123d"
RUN uv run --no-project --with ifcopenshell --with trimesh python -c "import ifcopenshell.geom"

CMD ["bash", "bench/fly/probe.sh"]
