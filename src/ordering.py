"""Модуль вычисления порядка загрузки зависимостей."""
from typing import Dict, List, Tuple


def load_order(
    repo: Dict[str, List[str]], root: str
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Возвращает порядок загрузки и список циклов."""
    if root not in repo:
        raise ValueError(f"Пакет '{root}' отсутствует в репозитории")

    """Цвета: 0 - не посещен, 1 - в процессе, 2 - обработан."""
    color: Dict[str, int] = {}
    order: List[str] = []
    cycles: List[Tuple[str, str]] = []

    color[root] = 1
    stack = [(root, iter(repo.get(root, [])))]

    while stack:
        node, it = stack[-1]
        try:
            nxt = next(it)
        except StopIteration:
            """Пост-обход: добавляем узел в порядок только после всех детей."""
            color[node] = 2
            order.append(node)
            stack.pop()
            continue

        if nxt not in repo:
            if color.get(nxt, 0) == 0:
                color[nxt] = 2
                order.append(nxt)
            continue

        col = color.get(nxt, 0)
        if col == 0:
            color[nxt] = 1
            stack.append((nxt, iter(repo.get(nxt, []))))
        elif col == 1:
            cycles.append((node, nxt))

    return order, cycles
