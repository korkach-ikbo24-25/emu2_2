"""Модуль загрузки тестового репозитория."""
from typing import Dict, List


class TestRepoError(Exception):
    """Ошибка загрузки тестового репозитория."""


def _is_valid_name(text: str) -> bool:
    """Проверяет, что имя состоит из заглавных латинских букв."""
    return bool(text) and text.isalpha() and text.isupper()


def _parse_line(line: str, line_num: int) -> tuple[str, List[str]]:
    """Разбирает одну строку формата 'NAME: DEP DEP ...'."""
    if ":" not in line:
        msg = f"Строка {line_num}: ожидался формат 'NAME: DEP'"
        raise TestRepoError(msg)

    name, _, rest = line.partition(":")
    name = name.strip()

    if not _is_valid_name(name):
        msg = f"Строка {line_num}: неверное имя '{name}'"
        raise TestRepoError(msg)

    deps = rest.split()
    invalid = next((d for d in deps if not _is_valid_name(d)), None)
    if invalid is not None:
        msg = f"Строка {line_num}: неверная зав. '{invalid}'"
        raise TestRepoError(msg)

    return name, deps


def _add_to_repo(repo: Dict[str, List[str]], name: str, deps: List[str],
                 line_num: int) -> None:
    """Добавляет запись в репозиторий, проверяя дубликаты."""
    if name in repo:
        msg = f"Строка {line_num}: повтор '{name}'"
        raise TestRepoError(msg)
    repo[name] = deps


def load_test_repo(path: str) -> Dict[str, List[str]]:
    """Читает файл 'A: B C' и возвращает словарь зависимостей."""
    repo: Dict[str, List[str]] = {}
    try:
        with open(path, encoding="utf-8") as file:
            for line_num, raw in enumerate(file, 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue

                name, deps = _parse_line(line, line_num)
                _add_to_repo(repo, name, deps, line_num)
    except FileNotFoundError:
        raise TestRepoError(f"Файл не найден: {path}")

    if not repo:
        raise TestRepoError(f"Репозиторий пуст: {path}")
    return repo
