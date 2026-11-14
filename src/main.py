"""Точка входа CLI-приложения."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_loader import ConfigError, load_config
from repo_apt import RepoError, load_repo_url


def print_config(cfg) -> None:
    """Выводит параметры конфигурации на экран."""
    print("=== Параметры конфигурации ===")
    print(f"  package    : {cfg.package}")
    print(f"  repo       : {cfg.repo}")
    print(f"  repo_mode  : {cfg.repo_mode}")
    print(f"  output     : {cfg.output}")
    print(f"  ascii_tree : {cfg.ascii_tree}")


def print_direct_deps(cfg) -> int:
    """Скачивает репозиторий и выводит прямые зависимости."""
    try:
        repo = load_repo_url(cfg.repo)
    except RepoError as err:
        print(f"[ОШИБКА РЕПОЗИТОРИЯ] {err}", file=sys.stderr)
        return 3

    direct = repo.get(cfg.package)
    if direct is None:
        msg = f"Пакет '{cfg.package}' не найден в индексе"
        print(f"[ОШИБКА] {msg}", file=sys.stderr)
        return 3

    print(f"\nПрямые зависимости '{cfg.package}':")
    if not direct:
        print("  (нет)")
    else:
        for dep in direct:
            print(f"  - {dep}")
    return 0


def main(argv: list[str]) -> int:
    """Главная функция программы."""
    path = argv[1] if len(argv) > 1 else "data/config.csv"
    
    try:
        cfg = load_config(path)
    except ConfigError as err:
        print(f"[ОШИБКА КОНФИГУРАЦИИ] {err}", file=sys.stderr)
        return 2

    print_config(cfg)

    if cfg.repo_mode == "url":
        return print_direct_deps(cfg)

    print("[ИНФО] Режим test будет добавлен на этапе 3", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))