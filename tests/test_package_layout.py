"""Package smoke tests."""


def test_package_imports() -> None:
    """The src-layout package can be imported."""
    import domain_services  # noqa: F401
