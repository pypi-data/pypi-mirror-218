import logging
from texttable import Texttable
from asciiplot import asciiize, Color
import typing_extensions  # TODO : add to requirements
import numpy as np
import sys
import time

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger()
logging.Formatter.converter = time.localtime
logger.setLevel(logging.INFO)


def set_log_decorator(level: int) -> callable:
    """
    Create decorator that changes the logging level for a given function
    Args:
        level: logging level

    Returns:
        log_decorator : specific decorator
    """

    def log_decorator(func):
        def wrapper_func(*args, **kwargs):
            currentLevel = logger.getEffectiveLevel()
            logger.setLevel(level)
            res = func(*args, **kwargs)
            logger.setLevel(currentLevel)
            return res

        return wrapper_func

    return log_decorator


def array_to_str(array: np.ndarray, row_title: str = "Expected", col_title: str = "Predicted") -> str:
    """
    From array, create a displayable string
    Args:
        array: each column represent a predicted class, each row an expected class
        row_title: Title to be displayed next to rows
        col_title: Title to be displayed next to columns
    Returns:
        table_str: confusion matrix as string
    """
    if array is None:
        table_str = ""
    else:
        col_size = 9

        if len(array) < 1:
            table_str = " No Matrix"
        elif len(array) > 50:
            table_str = f"Output dimension number is too high : {len(array)}"
        else:
            # Change size of output to fit table
            array[0, 1:] = [_l if len(_l) <= col_size else _l[:col_size - 3] + "..." for _l in array[0, 1:]]
            array[1:, 0] = [_l if len(_l) <= col_size else _l[:col_size - 3] + "..." for _l in array[1:, 0]]

            table = Texttable()
            table.add_rows(array, header=False)
            table.set_cols_width([col_size] * len(array))
            table.set_cols_align(["c"] * len(array))
            table.set_cols_dtype(["t"] * len(array))
            table_str = table.draw()
            table_list = table_str.split("\n")
            row_title_str = f"  {row_title}  "
            for idx, row in enumerate(table_list):
                if idx == int(len(table_list) / 2):
                    table_list[idx] = row_title_str + row
                else:
                    table_list[idx] = " " * len(row_title_str) + row
            offset = int((col_size + 3) * len(array) / 2)
            table_str = " " * (offset - 4 + len(row_title_str)) + f"{col_title}\n" + "\n".join(table_list)
    return table_str


def lines_to_str(*sequences, colors: list = None, title: str = "Title", x_title: str = "x_title",
                 y_title: str = "y_title") -> str:
    if colors is None:
        colors = [Color.DEFAULT] * len(sequences)
    max_point_nb = np.max([len(_seq) for _seq in sequences])
    plot_str = asciiize(
        *sequences,
        sequence_colors=colors,
        inter_points_margin=int(100 / max_point_nb),
        height=20,
        background_color=Color.GREY_7,
        title=title,
        title_color=Color.MEDIUM_PURPLE,
        label_color=Color.MEDIUM_PURPLE,
        x_axis_description=x_title,
        y_axis_description=y_title,
        y_axis_tick_label_decimal_places=2,
        center_horizontally=True
    )
    return plot_str
