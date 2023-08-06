# 12.8 In (ValueSet) https://cql.hl7.org/09-b-cqlreference.html#in-valueset


from typing import Union
from cqlpy._internal.operators.nullological.is_null import is_null

from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept
from cqlpy._internal.types.null import Some
from cqlpy._internal.types.valueset import Valueset


def in_valueset(argument: Some[Union[str, Code, Concept]], valueset: Valueset) -> bool:
    if is_null(argument):
        return False

    elif isinstance(argument, str):
        for valueset_code in valueset.codes:
            if argument == valueset_code:
                return True

    elif isinstance(argument, Code):
        for valueset_code in valueset.codes:
            if argument.code == valueset_code.code:
                return True

    elif isinstance(argument, Concept):
        for code in argument.codes:
            for valueset_code in valueset.codes:
                if code.code == valueset_code.code:
                    return True

    return False
