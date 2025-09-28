"""
Get esgvoc content
"""

import json

import esgvoc.api as ev


def main():
    """
    Get the data request content
    """
    reg_d = {}
    for data_descriptor in (
        "experiment",
        "source",
        # TODO: add more data descriptors
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
