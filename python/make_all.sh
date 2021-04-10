python3 dict_maker.py icc icc > ../results/dicts/icc_dict.py && python3 export_values.py icc icc > icc &&
python3 dict_maker.py gcc gcc > ../results/dicts/gcc_dict.py && python3 export_values.py gcc gcc > gcc &&
python3 dict_maker.py gcc_10 gcc_10 > ../results/dicts/gcc_10_dict.py && python3 export_values.py gcc_10 gcc_10 > gcc_10 &&
python3 dict_maker.py clang clang > ../results/dicts/clang_dict.py && python3 export_values.py clang clang > clang &&
python3 dict_maker.py sample_test sample_test > ../results/dicts/sample_test_dict.py && python3 export_values.py sample_test sample_test > sample_test
