"""Точка входа CLI-приложения."""
import sys
import os

# Добавляем папку src в путь, чтобы импорты работали
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_loader import ConfigError, load_config


def print_config(cfg) -> None:
    """Выводит параметры конфигурации на экран."""
    print("=== Параметры конфигурации ===")
    print(f"  package    : {cfg.package}")
    print(f"  repo       : {cfg.repo}")
    print(f"  repo_mode  : {cfg.repo_mode}")
    print(f"  output     : {cfg.output}")
    print(f"  ascii_tree : {cfg.ascii_tree}")


def main(argv: list[str]) -> int:
    """Главная функция программы."""
    path = argv[1] if len(argv) > 1 else "data/config.csv"
    
    try:
        cfg = load_config(path)
    except ConfigError as err:
        print(f"[ОШИБКА КОНФИГУРАЦИИ] {err}", file=sys.stderr)
        return 2

    print_config(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))