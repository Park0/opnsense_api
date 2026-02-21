try:
    from importlib.metadata import version
    __version__ = version("opnsense-api2")
except Exception:
    __version__ = "dev"
