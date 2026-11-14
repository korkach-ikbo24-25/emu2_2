"""Точка входа CLI-приложения."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_loader import ConfigError, load_config
from repo_apt import RepoError, load_repo_url
from repo_test import TestRepoError, load_test_repo
from graph import GraphError, build_graph
from ordering import load_order


def print_config(cfg) -> None:
    """Выводит параметры конфигурации на экран."""
    print("=== Параметры конфигурации ===")
    print(f"  package    : {cfg.package}")
    print(f"  repo       : {cfg.repo}")
    print(f"  repo_mode  : {cfg.repo_mode}")
    print(f"  output     : {cfg.output}")
    print(f"  ascii_tree : {cfg.ascii_tree}")


def load_repo(cfg):
    """Загружает данные (URL или тестовый файл)."""
    if cfg.repo_mode == "url":
        return load_repo_url(cfg.repo)
    return load_test_repo(cfg.repo)


def print_graph_summary(edges, nodes, cycles) -> None:
    """Выводит статистику по графу и найденные циклы."""
    total_edges = sum(len(v) for v in edges.values())
    print(f"\nУзлов в графе: {len(nodes)}")
    print(f"Рёбер в графе: {total_edges}")

    if cycles:
        print(f"Обнаружены циклы ({len(cycles)}):")
        for a, b in cycles:
            print(f"  {a} -> {b} (цикл)")
    else:
        print("Циклов не обнаружено")


def print_load_order(repo, package) -> None:
    """Выводит порядок установки пакетов."""
    seq, _ = load_order(repo, package)
    print("\nПорядок загрузки (зависимости раньше пакета):")
    for i, pkg in enumerate(seq, 1):
        print(f"  {i:>2}. {pkg}")


def main(argv: list[str]) -> int:
    """Главная функция программы."""
    path = argv[1] if len(argv) > 1 else "data/config.csv"
    
    try:
        cfg = load_config(path)
    except ConfigError as err:
        print(f"[ОШИБКА КОНФИГУРАЦИИ] {err}", file=sys.stderr)
        return 2

    print_config(cfg)

    try:
        repo = load_repo(cfg)
    except (RepoError, TestRepoError) as err:
        print(f"[ОШИБКА РЕПОЗИТОРИЯ] {err}", file=sys.stderr)
        return 3

    try:
        edges, nodes, cycles = build_graph(repo, cfg.package)
    except GraphError as err:
        print(f"[ОШИБКА ГРАФА] {err}", file=sys.stderr)
        return 4

    print_graph_summary(edges, nodes, cycles)
    print_load_order(repo, cfg.package)
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))