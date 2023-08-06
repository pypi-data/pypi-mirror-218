from collections import abc
from typing import Any

from cherre_singer_ingest.value_items import Record


def flatten_object(arg: Any) -> Record:
    """
    Helper method to take nested objects, and turn them into flat ones
    :param arg:
    :return:
    """
    dic = dict(arg)
    res = {}
    for key in dic:
        val = dic[key]
        if isinstance(val, abc.Mapping):
            sub_dic = flatten_object(val)
            for sub_key in sub_dic:
                res[f"{key}_{sub_key}"] = sub_dic[sub_key]
        else:
            res[key] = val

    return res
