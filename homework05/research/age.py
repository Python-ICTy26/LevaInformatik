import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def validate_bdate(bdate: str) -> bool:
    try:
        dt.datetime.strptime(bdate, '%d.%m.%Y')
        return True
    except Exception:
        return False


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id=user_id, fields=['bdate']).items

    ages = []

    for el in friends:
        if 'bdate' in el and validate_bdate(el['bdate']):
            ages.append(2022.0 - float(el['bdate'].split('.')[-1]))

    if len(ages) > 0:
        return statistics.median(ages)
