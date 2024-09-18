from numpy.typing import NDArray
import rpy2.robjects as ro
from typing import Any, Callable
import numpy as np

supported_classes = {"list", "array", "matrix", "vector", "atomic"}

def rcall(expr: str) -> Any:
    return ro.r(expr, print_r_warnings=False, invisible=True)


def get_rclass(x: Any) -> NDArray[np.unicode_] | None:
    from .function_wrapper import rfunc
    try:
        f: Callable | Any = rfunc("class")
        return np.asarray(f(x), dtype = "U")
    except:
        return None

def has_unsupported_rclass(x: Any) -> bool:
    rclass = get_rclass(x)

    if rclass is None or len(rclass.tolist()) == 0:
        return False
    if isinstance(rclass.tolist(), str):
        rclass = {rclass.tolist()}
    else:
        rclass = set(rclass.tolist())

    return len(rclass) > 0 and not rclass.issubset(supported_classes)
        

def as_matrix(x: Any, str = None) -> NDArray | Any:
    from .function_wrapper import rfunc
    f: Callable | Any = rfunc("as.matrix")
    return f(x)
