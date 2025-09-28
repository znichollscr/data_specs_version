"""
Test data request content against stored values
"""

from data_request_api.content import dump_transformation as dt
from data_request_api.query import data_request as dr


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


def get_data_request_content():
    """
    Get the data request content
    """
    DATA_REQUEST_VERSION = "v1.2.2"

    # Raw content in AirTable raw export form,
    # not that interesting probably
    # content = dc.load(version=DATA_REQUEST_VERSION)

    content_dict = dt.get_transformed_content(DATA_REQUEST_VERSION)
    data_request_obj = dr.DataRequest.from_separated_inputs(**content_dict)
    all_variables = data_request_obj.get_variables()
    # dreq_tables = dq.create_dreq_tables_for_request(
    #     content=content, dreq_version=DATA_REQUEST_VERSION
    # )

    # I am puzzled why`get_variables_metadata` has to be so complicated.
    # I would have assumed this could just be expressed in AirTable,
    # but it appears not.
    all_compound_names = [v.get("cmip6_compound_name").value for v in all_variables]
    all_compound_names = all_compound_names[:3]
    # all_metadata = dq.get_variables_metadata(
    #     content=dreq_tables,
    #     compound_names=all_compound_names,
    #     dreq_version=DATA_REQUEST_VERSION,
    # )

    # Someone can show me what I am doing wrong above later,
    # this can't be the right way to do this
    reg_vals_l = []
    # Don't export experiments, they're defined by esgvoc instead
    for v in all_variables:
        vd = get_value_as_dict(v)
        reg_vals_l.append(vd)

    res = {
        v["cmip6_compound_name"]: v
        for v in sorted(reg_vals_l, key=lambda x: x["cmip6_compound_name"])
    }

    return res


def test_data_request_content(data_regression):
    data_request_content = get_data_request_content()

    data_regression.check(data_request_content)
