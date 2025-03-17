FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir duckdb pandas

COPY read_data.py /app/
COPY queries.py /app/
COPY raw_data/ /app/raw_data/

COPY run_project.sh /app/
RUN chmod +x /app/run_project.sh

ENTRYPOINT ["/app/run_project.sh"]