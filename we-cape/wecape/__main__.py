"""Enable `python -m wecape` as the canonical CLI entry point."""

from wecape.capture.main import main

if __name__ == "__main__":
    main()
