import sys


def export_values(array):
    for i in array:
        for j in i:
            print(f"{format(i[j], '.6f')} '{j}'")
        print(f"")


# Pass values to export as command argument
set = sys.argv[1]

if set == 'clang':
    from clang_values import clang
    export_values(clang)
elif set == 'gcc':
    from gcc_values import gcc
    export_values(gcc)
elif set == 'gcc_10':
    from gcc_10_values import gcc_10
    export_values(gcc_10)
elif set == 'icc':
    from icc_values import icc
    export_values(icc)
