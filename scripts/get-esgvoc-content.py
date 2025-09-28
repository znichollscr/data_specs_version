"""
Get esgvoc content
"""

import json

import esgvoc.api as ev


def get_value_as_dict(value) -> str:
    """
    Get a value as a dict

    Required to handle magic DR types
    """
    value_dict = {}
    for a in value.attributes:
        if a in ("flag_-_variable_change_since_cmip6", "id", "uid"):
            continue

        tmp = value.get(a)
        if isinstance(tmp, list):
            value_dict[a] = []
            for v in tmp:
                if hasattr(v, "attributes") and v.attributes != v.name:
                    value_dict[a].append(get_value_as_dict(v))

                else:
                    value_dict[a].append(v.value)

        elif isinstance(tmp, str | int | float):
            value_dict[a] = tmp

        elif hasattr(tmp, "attributes") and tmp.attributes != tmp.value:
            value_dict[a] = get_value_as_dict(tmp)

        else:
            value_dict[a] = tmp.value

    return value_dict


def main():
    """
    Get the data request content
    """
    # TODO: add more
    reg_d = {}
    for data_descriptor in (
        "experiment",
        "source",
    ):
        reg_d[data_descriptor] = {
            v.id: v.model_dump()
            for v in ev.get_all_terms_in_data_descriptor(data_descriptor)
        }

    with open("esgvoc-vals.json", "w") as fh:
        json.dump(reg_d, fh, sort_keys=True, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main()
