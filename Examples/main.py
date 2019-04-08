from BrowserAutomator.setup import run
from logging import DEBUG

if __name__ == "__main__":
    run(["setup.yml"], ["loop.yml"], log_level=DEBUG)
