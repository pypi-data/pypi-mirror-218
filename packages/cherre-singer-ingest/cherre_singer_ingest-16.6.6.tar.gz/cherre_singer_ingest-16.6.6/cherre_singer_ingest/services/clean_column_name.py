from typing import Iterable, List


def clean_column_name(string: str, lowercase_schema: bool = False) -> str:
    if not string:
        raise ValueError("Empty column name in schema cannot be processed!")
    res = (
        string.strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
    )
    res = res.replace("#", "_num_").replace("!", "").replace("&", "_and_")
    res = res.replace(",", "_")

    if res[0].isdigit():
        res = "_" + res
    if lowercase_schema:
        res = res.lower()
    return res


def clean_column_names(
    names: Iterable[str], lowercase_schema: bool = False
) -> List[str]:
    # clean a collection of names, ensure there are no duplicates after doing so!
    clean_names = [clean_column_name(name) for name in names]
    de_duped = list(set(clean_names))
    de_duped.sort()
    return de_duped
