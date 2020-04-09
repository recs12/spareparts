import functools


class Colors:
    def electric(prp1, color):
        def _outer_wrapper(wrapped_function):
            @functools.wraps(wrapped_function)
            def _wrapper(*args, **kwargs):
                d, s = wrapped_function(*args, **kwargs)
                targeted_index = d.index[d.prp1.isin(prp1)].tolist()
                for row in targeted_index:
                    cellule = (
                        f"A{row+2}:U{row+2}"
                    )  # number 2 added for compensate lapse in excel file
                    s.range(cellule).color = color
                return (d, s)

            return _wrapper

        return _outer_wrapper

    def obsolete(color):
        def _outer_wrapper(wrapped_function):
            @functools.wraps(wrapped_function)
            def _wrapper(*args, **kwargs):
                d, s = wrapped_function(*args, **kwargs)
                targeted_index = d.index[d.ST.isin(["O", "U"])].tolist()
                for row in targeted_index:
                    cellule = (
                        f"J{row+2}"
                    )  # number 2 added for compensate lapse in excel file
                    s.range(cellule).color = color
                return (d, s)

            return _wrapper

        return _outer_wrapper

    def meter_foot(color):
        def _outer_wrapper(wrapped_function):
            @functools.wraps(wrapped_function)
            def _wrapper(*args, **kwargs):
                d, s = wrapped_function(*args, **kwargs)
                targeted_index = d.index[d.UOM.isin(["MT", "FT", "RL", "SF"])].tolist()
                for row in targeted_index:
                    cellule = (
                        f"I{row+2}"
                    )  # number 2 added for compensate lapse in excel file
                    s.range(cellule).color = color
                return (d, s)

            return _wrapper

        return _outer_wrapper

    electric = staticmethod(electric)
    obsolete = staticmethod(obsolete)
    meter_foot = staticmethod(meter_foot)
