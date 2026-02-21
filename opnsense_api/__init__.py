try:
    from importlib.metadata import version
    __version__ = version("opnsense-api")
except Exception:
    __version__ = "dev"
