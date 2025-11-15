"""Module entry point for ``python -m studon_downloader``."""

from __future__ import annotations

from importlib import import_module



def _import_create_gui():
    """Import ``create_gui`` regardless of how the module is executed.

    When the package is executed via ``python -m studon_downloader`` the
    ``__package__`` attribute is populated and a standard relative import works.
    However, when PyInstaller executes the generated ``__main__`` file it does
    not set ``__package__`` which causes the relative import to fail with
    ``ImportError: attempted relative import with no known parent package``.

    To keep both execution paths working we attempt the relative import first
    and fall back to importing the sibling module directly via its fully
    qualified name.
    """

    if __package__:
        from .gui import create_gui  # type: ignore[import-not-found]
        return create_gui

    module = import_module("studon_downloader.gui")
    return module.create_gui

def main() -> None:
    create_gui = _import_create_gui()
    app = create_gui()
    app.run()


if __name__ == "__main__":
    main()
