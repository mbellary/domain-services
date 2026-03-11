# Domain Services

Repository scaffold for a forex ML domain service.

## Development with uv

This repository is configured as a **uv-managed Python package** with a `src/` layout.

### Quick start

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
```

### Package layout

Python source code lives under:

- `src/domain_services/`
- `tests/`
