"""Модуль построения графа зависимостей."""
from typing import Dict, Iterator, List, Tuple


class GraphError(Exception):
    """Ошибка построения графа."""


def _add_edge(
    edges: Dict[str, List[str]], node: str, nxt: str
) -> None:
    """Добавляет ребро node -> nxt, если его ещё нет."""
    edges.setdefault(node, [])
    if nxt not in edges[node]:
        edges[node].append(nxt)


def _visit_child(
    repo: Dict[str, List[str]],
    color: Dict[str, int],
    order: List[str],
    stack: List[Tuple[str, Iterator[str]]],
    node: str,
    nxt: str,
) -> None:
    """Обрабатывает переход к соседу nxt из узла node."""
    col = color.get(nxt, 0)
    if col != 0:
        return
    color[nxt] = 1
    order.append(nxt)
    stack.append((nxt, iter(repo.get(nxt, []))))


def _step(
    repo: Dict[str, List[str]],
    color: Dict[str, int],
    edges: Dict[str, List[str]],
    order: List[str],
    cycles: List[Tuple[str, str]],
    stack: List[Tuple[str, Iterator[str]]],
) -> bool:
    """Делает один шаг DFS. Возвращает False, когда стек опустел."""
    node, it = stack[-1]
    try:
        nxt = next(it)
    except StopIteration:
        color[node] = 2
        stack.pop()
        return bool(stack)

    if nxt not in repo:
        edges.setdefault(node, [])
        return True

    _add_edge(edges, node, nxt)
    if color.get(nxt, 0) == 1:
        cycles.append((node, nxt))
    else:
        _visit_child(repo, color, order, stack, node, nxt)
    return True


def build_graph(
    repo: Dict[str, List[str]], root: str
) -> Tuple[Dict[str, List[str]], List[str], List[Tuple[str, str]]]:
    """Строит граф итеративным DFS.

    Цвета: 0 - не посещён, 1 - в процессе, 2 - обработан.
    """
    if root not in repo:
        raise GraphError(f"Пакет '{root}' отсутствует в репозитории")

    color: Dict[str, int] = {root: 1}
    edges: Dict[str, List[str]] = {}
    order: List[str] = [root]
    cycles: List[Tuple[str, str]] = []
    stack: List[Tuple[str, Iterator[str]]] = [
        (root, iter(repo.get(root, [])))
    ]

    while stack:
        _step(repo, color, edges, order, cycles, stack)

    return edges, order, cycles
