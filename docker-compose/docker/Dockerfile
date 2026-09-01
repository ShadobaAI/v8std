FROM python:3.12-slim

WORKDIR /opt/v8std

RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/v8std/requirements.txt
COPY requirements-mcp.txt /opt/v8std/requirements-mcp.txt
COPY scripts /opt/v8std/scripts

# BEGIN V8STD-FORK
# Windows checkout may use CRLF; container entry points require LF.
RUN find /opt/v8std/scripts -type f -name '*.sh' -exec sed -i 's/\r$//' {} +

# END V8STD-FORK
RUN chmod +x /opt/v8std/scripts/generate_social_cards.py \
    /opt/v8std/scripts/generate_search_vectors.py \
    /opt/v8std/scripts/install_zensical.sh \
    /opt/v8std/scripts/run_v8std_mcp.sh \
    /opt/v8std/scripts/v8std_mcp_server.py \
    /opt/v8std/scripts/zensical_docs.sh \
    && /opt/v8std/scripts/install_zensical.sh \
    && python -m pip install --upgrade -r /opt/v8std/requirements-mcp.txt

WORKDIR /docs

ENTRYPOINT ["/opt/v8std/scripts/zensical_docs.sh"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
