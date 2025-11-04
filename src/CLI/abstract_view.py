from abc import ABC, abstractmethod


class AbstractView(ABC):
    def __init__(self, session, services: dict):
        self.session = session
        self.services = services

    @abstractmethod
    def display(self) -> None:
        pass

    def prompt(self, message: str) -> str:
        try:
            return input(message)
        except (KeyboardInterrupt, EOFError):
            print()
            return ""

    def print_error(self, message: str):
        print(f"[ERROR] {message}")

    def print_info(self, message: str):
        print(f"[INFO] {message}")
