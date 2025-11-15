"""Module entry point for ``python -m studon_downloader``."""

from .gui import create_gui


def main() -> None:
    app = create_gui()
    app.run()


if __name__ == "__main__":
    main()
