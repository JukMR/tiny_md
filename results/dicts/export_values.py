from clang_values import clang
from gcc_values import gcc
from gcc_10_values import gcc_10
from icc_values import icc


def export_values(array):
    for i in array:
        for j in i:
            print(f"{format(i[j], '.6f')} '{j}'")
        print(f"")


export_values(clang)
