FROM nixos/nix as builder

RUN nix-channel --update && \
    nix-shell -p \
      python311Packages.pytest \
      python311Packages.sqlalchemy \
      python311Packages.psycopg2 \
      python311Packages.requests \
      python311Packages.fastapi \
      python311Packages.pydantic \
      python311Packages.uvicorn \
      python311Packages.pika \
      python311Packages.python-dotenv --run "exit"

FROM scratch

COPY --from=builder / /

WORKDIR /app
COPY . /app
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]