from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.db import Base


def convert_filter_by(model_class: type["Base"], filter_by: str) -> list:
    """TODO: write input / output docs"""
    if filter_by is not None and filter_by != "null":
        criteria = dict(x.strip().split("=") for x in filter_by.split(","))

        criteria_list = []
        for attr, value in criteria.items():
            if _attr := getattr(model_class, attr, None):
                if attr.endswith("id"):
                    criteria_list.append(_attr == value)
                else:
                    search = f"%{value}%"
                    criteria_list.append(_attr.ilike(search))

        return criteria_list

    return []


def convert_sort_by(model_class: type["Base"], sort_by: str):
    """TODO: write input / output docs"""
    sort_fields = sort_by.split(",")
    sort_criteria = []
    for field_direction in sort_fields:
        field, direction = field_direction.split(":")
        if _attr := getattr(model_class, field, None):
            if direction == "asc":
                sort_criteria.append(_attr.asc())
            elif direction == "desc":
                sort_criteria.append(_attr.desc())

    return sort_criteria
