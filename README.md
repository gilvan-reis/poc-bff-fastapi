# poc-bff-fastapi

Code used to test the utilization of the [fastapi](https://fastapi.tiangolo.com/) as a BFF for Méliuz.

In this POC, I have included:
- multiple HTTP requests with aggregation.
- query, header, and JWT authorization.
- password hashing.
- memory cache with cache invalidation.

## Requirements

- Docker (version used `20.10.5`).
- Docker (version used `1.27.4`).
- Makefile (version used `4.1`).

## Quick Start

1. Use `make build` to build the image.
1. Use `make up` to up the container.
    - Alternatively, use `make up-silent` to up the container in the background. You can use
    `make logs` to view the container logs
1. Access http://127.0.0.1:3021/docs and make requests.
1. Use `make down` to stop the container.
