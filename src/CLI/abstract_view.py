from typing import Any, Dict

from src.CLI.session import Session


class AbstractView:
    def __init__(self, session: Session, services: Dict[str, Any]):
        self.session = session
        self.services = services

    def display(self) -> None:
        raise NotImplementedError()

    def prompt(self, msg: str = "> ") -> str:
        try:
            return input(msg).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            return ""

    def print_info(self, msg: str) -> None:
        print(f"[INFO] {msg}")

    def print_error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")
