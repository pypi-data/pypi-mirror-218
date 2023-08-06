# 12.8 In (ValueSet) https://cql.hl7.org/09-b-cqlreference.html#in-valueset


from typing import Union
from cqlpy._internal.operators.clinical.in_valueset import in_valueset
from cqlpy._internal.operators.nullological.is_null import is_null

from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept
from cqlpy._internal.types.null import Some
from cqlpy._internal.types.valueset import Valueset


def any_in_valueset(
    argument: list[Some[Union[str, Code, Concept]]], valueset: Valueset
) -> bool:
    if not is_null(argument):
        for item in argument:
            if in_valueset(item, valueset):
                return True

    return False
