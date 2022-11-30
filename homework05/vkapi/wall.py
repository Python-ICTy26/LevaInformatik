import textwrap
import time
import math
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize

from vkapi import config, session
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    pass


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    if count > max_count:
        temp = []

        for i in range(math.ceil(count // max_count)):
            temp += get_wall_execute(owner_id=owner_id, domain=domain, offset=max_count*i, count=count-max_count,max_count=max_count, filter=filter, extended=extended, fields=fields)
            time.sleep(0.5)

        return temp

    code = f"""
        var requestsCounter = 0;
        const baseOffset = {offset};

        var items = [];

        while (requestsCounter < 25) {{
            const result = API.wall.get({{
                "owner_id": "{owner_id}",
                "domain": "{domain}",
                "offset": {count} * requestsCounter + baseOffset,
                "count":"{count}",
                "filter": "{filter}",
                "extended": {extended},
                "fields": {fields}
            }});

            requestsCounter = requestsCounter + 1;
            lastRecordsReturned = result@.count;
            items.push(result@.items);
        }}

        return items;

    """

    result = session.post('execute', data=code).json()['response']
    return json_normalize(result['items'])
