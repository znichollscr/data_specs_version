"""
Test esgvoc content against stored values
"""

from esgvoc.apps.cmor_tables import generate_cvs_table


def get_esgvoc_content():
    res = generate_cvs_table(project="cmip7").to_cvs_json()

    return res


def test_esgvoc_content(data_regression):
    esgvoc_content = get_esgvoc_content()

    data_regression.check(esgvoc_content)
