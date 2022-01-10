from itertools import groupby
from typing import Any, List, Tuple

import text
from dataholders.finger import Finger
from dataholders.mistake import Mistake, Mistakes


def mistakes_formatted(
    mistakes: Mistakes,
    only_headers: bool = False,
    compact: bool = True,
    skip_if_less: int = 0,
) -> str:
    result = ""
    format_finger_details = compact_format if compact else detailed_format
    header = text.finger_header_dot if only_headers else text.finger_header_semicolon
    for finger, finger_mistakes in group_by_finger(mistakes):
        result += header.format(finger, len(finger_mistakes))
        if only_headers:
            continue
        result += format_finger_details(finger_mistakes, skip_if_less)
        result += "\n"
    return result


def detailed_format(finger_mistakes: Mistakes, skip_if_less: int = 0) -> str:
    result = ""
    for mistake, group in group_by_mistake(finger_mistakes):
        if result and skip_if_less and len(group) < skip_if_less:
            result += text.skip_if_less_indication
            break
        result += text.mistakes_detailed_stat.format(
            actual=mistake.actual, expected=mistake.expected, times=len(group)
        )
    return result


def compact_format(finger_mistakes: Mistakes, skip_if_less: int = 0) -> str:
    result = ""
    for expected, group in group_by_expected(finger_mistakes):
        if result and skip_if_less and len(group) < skip_if_less:
            result += text.skip_if_less_indication
            break
        actual = set("'{0}'".format(mistake.actual) for mistake in group)
        result += text.mistakes_compact_stat.format(
            actual=", ".join(actual), expected=expected, times=len(group)
        )
    return result


def group_by_finger(data: Mistakes) -> List[Tuple[Finger, Mistakes]]:
    gpd = [
        (finger, list(mistakes))
        for finger, mistakes in groupby(
            sorted(data, key=_key_expected_combined),
            key=_key_expected_finger,
        )
    ]
    return sorted(gpd, key=_key_group_size, reverse=True)


def group_by_mistake(data: Mistakes) -> List[Tuple[Mistake, Mistakes]]:

    gpd = [
        (mistake, list(group))
        for mistake, group in groupby(sorted(data, key=_key_actual))
    ]
    return sorted(gpd, key=_key_group_size_and_actual, reverse=True)


def group_by_expected(data: Mistakes) -> List[Tuple[str, Mistakes]]:
    gpd = [
        (mistake, list(group))
        for mistake, group in groupby(
            sorted(data, key=_key_expected), key=_key_expected
        )
    ]
    return sorted(gpd, key=_key_group_size, reverse=True)


def _key_group_size_and_actual(group: Tuple[Mistake, Mistakes]):
    return (len(group[1]), group[0].actual)


def _key_group_size(group: Tuple[Any, Mistakes]):
    return len(group[1])


def _key_actual(m: Mistake) -> str:
    return m.actual


def _key_expected(m: Mistake) -> str:
    return m.expected


def _key_expected_finger(m: Mistake) -> Finger:
    return m.finger_expected


def _key_expected_combined(m: Mistake) -> Tuple[Finger, str]:
    return (m.finger_expected, m.expected)
