"""
Test esgvoc content against stored values
"""

import esgvoc.api as ev


def get_esgvoc_content():
    res = {}
    for data_descriptor in (
        "experiment",
        "source",
        # TODO: add more data descriptors
    ):
        res[data_descriptor] = {
            v.id: v.model_dump()
            for v in ev.get_all_terms_in_data_descriptor(data_descriptor)
        }

    return res


def test_esgvoc_content(data_regression):
    esgvoc_content = get_esgvoc_content()

    data_regression.check(esgvoc_content)
