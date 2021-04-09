import sys


def export_values(array):
    for i in array:
        for j in i:
            print(f"{format(i[j], '.6f')} '{j}'")
        print(f"")


# Pass values to export as command argument
set = sys.argv[1]

tmp = sys.path
sys.path.append('../results/dicts/')
if set == 'clang':
    from clang_dict import clang
    export_values(clang)
elif set == 'gcc':
    from gcc_dict import gcc
    export_values(gcc)
elif set == 'gcc_10':
    from gcc_10_dict import gcc_10
    export_values(gcc_10)
elif set == 'icc':
    from icc_dict import icc
    export_values(icc)
elif set == 'sample_test':
    from sample_test_dict import sample_test
    export_values(sample_test)

sys.path = tmp
