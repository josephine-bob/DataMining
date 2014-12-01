import matplotlib.pyplot as plt
from StringIO import StringIO
import numpy as np


def convert_into_integer(list1):
    """
    parsing and converting employees list
    from dbpedia and in strings
    to a list of integer
    >>> convert_into_integer(['1'])
    [1]
    """
    converted_list = []
    for element in list1:
        element = int(element)
        converted_list.append(element)
    return converted_list


def triple_correlate(list1, list2, list3):
    """
    return correlation matrix for the 3 lists given
    """
    final_list = []
    final_list.append(list1)
    final_list.append(list2)
    final_list.append(list3)

    return np.corrcoef(final_list)


def scatter_plot(list1, list2):
    """
    do the scatter plot of 2 lists
    """
    plt.scatter(list1, list2)
    sio = StringIO()
    plt.savefig(sio)
    return sio.getvalue().encode('base64')[:-1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
