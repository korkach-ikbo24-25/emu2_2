"""Простые тесты для модуля repo_apt (без unittest)."""
import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "src"
))

from repo_apt import _parse_dep_field, parse_packages


def check_simple():
    """Проверка простого списка зависимостей."""
    result = _parse_dep_field("libc6 (>= 2.34), dpkg")
    assert result == ["libc6", "dpkg"], f"Ошибка: {result}"


def check_alternatives():
    """Проверка альтернатив (через |)."""
    result = _parse_dep_field("a | b, c:any")
    assert result == ["a", "b", "c"], f"Ошибка: {result}"


def check_multiline():
    """Проверка склейки переносов строк в Depends."""
    text = (
        "Package: test\n"
        "Depends: libc6 (>= 2.34),\n"
        " libgcc-s1 (>= 3.0)\n"
    )
    result = parse_packages(text)
    assert result["test"] == ["libc6", "libgcc-s1"], f"Ошибка: {result}"


if __name__ == "__main__":
    print("Запуск тестов...")
    try:
        check_simple()
        check_alternatives()
        check_multiline()
        print("Все 3 теста пройдены успешно! OK.")
    except AssertionError as err:
        print(f"Тест провален: {err}")
        sys.exit(1)