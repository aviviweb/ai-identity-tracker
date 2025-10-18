try:
    from app.main import app  # noqa: F401
    print("import_ok")
except Exception as exc:
    print(f"import_failed: {exc}")


