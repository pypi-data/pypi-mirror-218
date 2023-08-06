# Subclass of list with more than 100 useful methods - pure Python 
 
## pip install mehrlist

### All dependencies are pure Python


 ```python
 |  append(self, o)
 |      Append object to the end of the list.
 |  
 |  appendleft(self, v)
 |  
 |  bisect_category_mapping(self, cats)
 |  
 |  bisect_leftmost_value_equal_to(self, n)
 |  
 |  bisect_leftmost_value_greater_than(self, n)
 |  
 |  bisect_leftmost_value_greater_than_or_equal(self, n)
 |  
 |  bisect_rightmost_value_equal_to(self, n)
 |  
 |  bisect_rightmost_value_less_than(self, n)
 |  
 |  bisect_rightmost_value_less_than_or_equal(self, n)
 |  
 |  convert_all_to_nested_list(self)
 |  
 |  convert_to_list(self)
 |  
 |  count_all_items(self)
 |  
 |  del_items(self, value)
 |  
 |  extend(self, other) -> None
 |      Extend list by appending elements from the iterable.
 |  
 |  extendleft(self, other)
 |  
 |  find_common_start_string(self)
 |  
 |  find_sequence(self, seq: tuple, distance_tolerance=0)
 |  
 |  flatten(self)
 |  
 |  flatten_and_group_by(self, func, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  flatten_level(self, n=None, dict_treatment='items', consider_non_iter=(<class 'str'>, <class 'bytes'>))
 |  
 |  flatten_with_index(self)
 |  
 |  get_cycle_list_until_every_list_fits(self, maxresults=5, append=False)
 |  
 |  get_iter_2_cycle_second_until_first_done(self, other)
 |  
 |  get_iter_add_one_item_each_iteration(self)
 |  
 |  get_iter_add_one_item_each_iteration_reverse(self)
 |  
 |  get_iter_batch(self, n)
 |  
 |  get_iter_call_function_over_and_over_with_new_value(self, f)
 |      https://github.com/joelgrus/stupid-itertools-tricks-pydata/blob/master/src/stupid_tricks.py
 |  
 |  get_iter_cycle_shortest(self, other)
 |  
 |  get_iter_enumerated_unpacked(self)
 |  
 |  get_iter_every_nth_element(self, step=2)
 |  
 |  get_iter_find_same_beginning_elements(self)
 |  
 |  get_iter_find_same_ending_elements(self)
 |  
 |  get_iter_item_difference(self)
 |  
 |  get_iter_list_ljust_rjust(self, ljust=0, ljustchr=' ', rjust=0, rjustchr=' ', getmax=True)
 |  
 |  get_iter_log_split(self)
 |  
 |  get_iter_nested(self)
 |  
 |  get_iter_nested_for_loop(self)
 |  
 |  get_iter_nested_for_loop_enumerated(self)
 |  
 |  get_iter_nested_one_ahead(self)
 |  
 |  get_iter_nested_with_path(self)
 |  
 |  get_iter_random_values_from_iter_endless(self)
 |  
 |  get_iter_reverse_lists_of_list(self)
 |  
 |  get_iter_rotate_left(self, n, onlyfinal=False)
 |  
 |  get_iter_rotate_right(self, n, onlyfinal=False)
 |  
 |  get_iter_stop_when_next_item_is_duplicate(self)
 |      https://github.com/joelgrus/stupid-itertools-tricks-pydata/blob/master/src/stupid_tricks.py
 |  
 |  get_iter_transposed_list_of_lists(self)
 |  
 |  get_iter_windowed(self, n)
 |  
 |  get_iter_windowed_distance(self, fillvalue=None, distance=1)
 |  
 |  get_levenshtein_distance(self, strings)
 |  
 |  get_normalized_list_of_lists(self, fillv=None)
 |  
 |  get_random_not_repeating_values(self, howmany)
 |  
 |  get_random_values_with_max_rep(self, howmany, maxrep)
 |  
 |  get_shuffle_copied_list(self)
 |  
 |  group_by(self, func, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  group_coordinates_by_distance(self, coordlist, limit_x, limit_y, continue_on_exceptions=True)
 |  
 |  group_intersections(self, keep_duplicates=False)
 |  
 |  group_sequences(self, fu)
 |  
 |  group_values_in_flattened_nested_iter_and_count(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_almost_equal(self, value, equallimit, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_bigger_than(self, number, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_bigger_than_or_equal(self, number, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_can_be_divided_by(self, div, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_ceil(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_coords_almost_equal(self, x_coord, y_coord, limit_x, limit_y, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_decoding_result(self, mode='strict', continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_division_remainder(self, div, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_divisor(self, div, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_element_pos(self, pos, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_endswith(self, n, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_equal(self, number, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_euclid_dist(self, coord, mindistance=0, maxdistance=500, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_even_odd(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_file_extension(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_files_folder_link(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_first_item(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_first_occurrence_in_string(self, char, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_floor(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_frequency(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_is_integer(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isalnum(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isalpha(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isascii(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isdecimal(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isdigit(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isidentifier(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isin(self, value, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isiter(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_islower(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isna(self, emptyiters: bool = False, nastrings: bool = False, emptystrings: bool = False, emptybytes: bool = False, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isnumeric(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isprintable(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isspace(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_istitle(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_isupper(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_last_occurrence_in_string(self, char, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_less_than(self, number, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_less_than_or_equal(self, number, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_literal_eval_type(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_percentage(self, percent_true, group1=True, group2=False, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_regular_expression_matches(self, regexpressions, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_round(self, n, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_startswith(self, n, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_string_length(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_substring(self, substrings, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_sum(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_sys_size(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_type(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_valid_url(self, continue_on_exceptions=True, withindex=False, withvalue=True)
 |  
 |  groupby_words_in_texts(self, wordlist, case_sen=False, continue_on_exceptions=True, withindex=False, boundary_right=True, boundary_left=True, withvalue=True)
 |  
 |  index_all(self, n)
 |  
 |  insert(self, index, value) -> None
 |      Insert object before index.
 |  
 |  list_of_tuples_to_family_tree(self, main_mapping_keys=(), bi_rl_lr='bi')
 |  
 |  number_of_combinations(self, k)
 |      from https://stackoverflow.com/a/48612518/15096247
 |      Number of combinations of length *k* of the elements of *it*.
 |  
 |  popleft(self)
 |  
 |  remove_duplicates(self)
 |  
 |  repeat_items(self, reps)
 |  
 |  reshape(self, how)
 |  
 |  search(self, value)
 |  
 |  shape_repeat(self, shape)
 |  
 |  sorted(self, func, reverse=False)
 |  
 |  split_by_indices(self, indices)
 |  
 |  to_nested_dict(self)
 
 
import math
import random
import sys

from mehrlist import NestedList

li = NestedList(
    [
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
        [[1, 2], [3, 4]],
    ],
    maxsize=30,
)
li.convert_all_to_nested_list()
li.to_nested_dict()
#
# Out[3]:
# {0: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  1: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  2: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  3: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  4: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  5: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  6: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  7: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  8: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  9: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  10: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}},
#  11: {0: {0: 1, 1: 2}, 1: {0: 3, 1: 4}}}
li.flatten()
# Out[4]: [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
li.flatten_with_index()
# Out[5]:
# [((0, 0, 0), 1), ((0, 0, 1), 2), ((0, 1, 0), 3), ((0, 1, 1), 4), ((1, 0, 0), 1), ((1, 0, 1), 2), ((1, 1, 0), 3), ((1, 1, 1), 4), ((2, 0, 0), 1), ((2, 0, 1), 2),
# ((2, 1, 0), 3), ((2, 1, 1), 4), ((3, 0, 0), 1), ((3, 0, 1), 2), ((3, 1, 0), 3), ((3, 1, 1), 4), ((4, 0, 0), 1), ((4, 0, 1), 2), ((4, 1, 0), 3), ((4, 1, 1), 4),
# ((5, 0, 0), 1), ((5, 0, 1), 2), ((5, 1, 0), 3), ((5, 1, 1), 4), ((6, 0, 0), 1), ((6, 0, 1), 2), ((6, 1, 0), 3), ((6, 1, 1), 4), ((7, 0, 0), 1), ((7, 0, 1), 2),
# ((7, 1, 0), 3), ((7, 1, 1), 4), ((8, 0, 0), 1), ((8, 0, 1), 2), ((8, 1, 0), 3), ((8, 1, 1), 4), ((9, 0, 0), 1), ((9, 0, 1), 2), ((9, 1, 0), 3), ((9, 1, 1), 4),
# ((10, 0, 0), 1), ((10, 0, 1), 2), ((10, 1, 0), 3), ((10, 1, 1), 4), ((11, 0, 0), 1), ((11, 0, 1), 2), ((11, 1, 0), 3), ((11, 1, 1), 4)]
li.remove_duplicates()
# Out[6]: [[[1, 2], [3, 4]]]
li.sorted(len)
# Out[7]:
# [[[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3,
# 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 2], [3, 4]]]
try:
    n = NestedList(1)
except TypeError:
    n = NestedList(1, convert_all=True)
print(n)
l = NestedList(range(50))
l.split_by_indices([2, 24, 48])
# [[0, 1], [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
# 41, 42, 43, 44, 45, 46, 47], [48, 49]]
list(l.get_iter_every_nth_element(9))
# Out[8]: [0, 9, 18, 27, 36, 45]
l.repeat_items(5)
# [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, ...]
list(l.get_iter_windowed(n=4))
# Out[12]:
# [(0, 1, 2, 3),
#  (1, 2, 3, 4),
#  (2, 3, 4, 5),
#  (3, 4, 5, 6),
list(l.get_iter_batch(3))
# Out[14]:
# [[0, 1, 2],
#  [3, 4, 5],
#  [6, 7, 8],
#  [9, 10, 11],

list(li.get_iter_nested_for_loop())[:2]
# Out[19]:
# [([1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2]),
#  ([1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [3, 4])]


list(li.get_iter_nested_for_loop_enumerated())[:2]
# Out[20]:
# [(0,
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2]),
#  (1,
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [1, 2],
#   [3, 4])]

list(l.get_iter_add_one_item_each_iteration())[:5]
# Out[22]: [[0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]]


list(l.get_iter_add_one_item_each_iteration_reverse())[:5]
# Out[23]: [[49], [48, 49], [47, 48, 49], [46, 47, 48, 49], [45, 46, 47, 48, 49]]

l2 = NestedList(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
        [13, 14, 15],
        [16, 17, 18],
        [19, 20, 21],
    ]
)
l3 = NestedList(
    [
        [[1, 2, 3], [4, 5, 6]],
        [[7, 8, 9], [10, 11, 12]],
        [[13, 14, 15], [16, 17, 18], [19, 20, 21]],
    ]
)

list(l3.get_iter_nested())
# Out[3]:
# [[[[1, 2, 3], [4, 5, 6]], [1, 2, 3], 1],
#  [[[1, 2, 3], [4, 5, 6]], [1, 2, 3], 2],
#  [[[1, 2, 3], [4, 5, 6]], [1, 2, 3], 3],
#  [[[1, 2, 3], [4, 5, 6]], [4, 5, 6], 4],
#  [[[1, 2, 3], [4, 5, 6]], [4, 5, 6], 5],
#  [[[1, 2, 3], [4, 5, 6]], [4, 5, 6], 6],
#  [[[7, 8, 9], [10, 11, 12]], [7, 8, 9], 7],
#  [[[7, 8, 9], [10, 11, 12]], [7, 8, 9], 8],
#  [[[7, 8, 9], [10, 11, 12]], [7, 8, 9], 9],
#  [[[7, 8, 9], [10, 11, 12]], [10, 11, 12], 10],
#  [[[7, 8, 9], [10, 11, 12]], [10, 11, 12], 11],
#  [[[7, 8, 9], [10, 11, 12]], [10, 11, 12], 12],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [13, 14, 15], 13],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [13, 14, 15], 14],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [13, 14, 15], 15],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [16, 17, 18], 16],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [16, 17, 18], 17],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [16, 17, 18], 18],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [19, 20, 21], 19],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [19, 20, 21], 20],
#  [[[13, 14, 15], [16, 17, 18], [19, 20, 21]], [19, 20, 21], 21]]

list(l3.get_iter_nested_with_path())
# Out[3]:
# [[((0,), [[1, 2, 3], [4, 5, 6]]), ((0, 0), [1, 2, 3]), ((0, 0, 0), 1)],
#  [((0,), [[1, 2, 3], [4, 5, 6]]), ((0, 0), [1, 2, 3]), ((0, 0, 1), 2)],
#  [((0,), [[1, 2, 3], [4, 5, 6]]), ((0, 0), [1, 2, 3]), ((0, 0, 2), 3)],
#  [((0,), [[1, 2, 3], [4, 5, 6]]), ((0, 1), [4, 5, 6]), ((0, 1, 0), 4)],

l4 = NestedList([[1, 2, 3, 4], [5, 1, 2, 3, 4], [55, 55, 1, 2, 3, 4]])
list(l4.get_iter_find_same_ending_elements())
# Out[4]: [1, 2, 3, 4]
l5 = NestedList(["ababa", "abacxxx", "abdd"])
list(l5.get_iter_find_same_beginning_elements())
# ['a', 'b']


l.reshape([20, [25], {1}, ((1,), 3)])
# Out[11]:
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
# 42, 43, 44], {45}, ((46,), 47, 48, 49)]


list(l4.get_iter_rotate_left(3))
# Out[14]:
# [['abacxxx', 'abdd', 'ababa'],
#  ['abdd', 'ababa', 'abacxxx'],
#  ['ababa', 'abacxxx', 'abdd']]

list(l4.get_iter_rotate_right(3))
# Out[15]:
# [['abdd', 'ababa', 'abacxxx'],
#  ['abacxxx', 'abdd', 'ababa'],
#  ['ababa', 'abacxxx', 'abdd']]


l4.shape_repeat((3, 4))

# Out[17]:
# [[['ababa', 'abacxxx', 'abdd'], ['ababa', 'abacxxx', 'abdd'], ['ababa', 'abacxxx', 'abdd']], [['ababa', 'abacxxx', 'abdd'], ['ababa', 'abacxxx', 'abdd'],
# ['ababa', 'abacxxx', 'abdd']], [['ababa', 'abacxxx', 'abdd'], ['ababa', 'abacxxx', 'abdd'], ['ababa', 'abacxxx', 'abdd']], [['ababa', 'abacxxx', 'abdd'],
# ['ababa', 'abacxxx', 'abdd'], ['ababa', 'abacxxx', 'abdd']]]


list(l2.get_iter_enumerated_unpacked())
# Out[19]:
# [(0, 1, 4, 7, 10, 13, 16, 19),
#  (1, 2, 5, 8, 11, 14, 17, 20),
#  (2, 3, 6, 9, 12, 15, 18, 21)]


list(l2.get_iter_cycle_shortest(range(10)))
# Out[21]:
# [([1, 2, 3], 0),
#  ([4, 5, 6], 1),
#  ([7, 8, 9], 2),
#  ([10, 11, 12], 3),
#  ([13, 14, 15], 4),
#  ([16, 17, 18], 5),
#  ([19, 20, 21], 6),
#  ([1, 2, 3], 7),
#  ([4, 5, 6], 8),
#  ([7, 8, 9], 9)]

list(l2.get_iter_reverse_lists_of_list())
# Out[3]:
# [[3, 2, 1],
#  [6, 5, 4],
#  [9, 8, 7],
#  [12, 11, 10],
#  [15, 14, 13],
#  [18, 17, 16],
#  [21, 20, 19]]

l6 = NestedList([1, 2, 3, 4, 5, 6, 7, 8, 8, 9, 0])
list(l6.get_iter_stop_when_next_item_is_duplicate())
# Out[4]: [1, 2, 3, 4, 5, 6, 7, 8]


list(l4.get_iter_nested_one_ahead())
# Out[8]:
# [[[[1, 2, 3, 4], 1], [[1, 2, 3, 4], 2]],
#  [[[1, 2, 3, 4], 2], [[1, 2, 3, 4], 3]],
#  [[[1, 2, 3, 4], 3], [[1, 2, 3, 4], 4]],
#  [[[1, 2, 3, 4], 4], [[5, 1, 2, 3, 4], 5]],
#  [[[5, 1, 2, 3, 4], 5], [[5, 1, 2, 3, 4], 1]],
#  [[[5, 1, 2, 3, 4], 1], [[5, 1, 2, 3, 4], 2]],
#  [[[5, 1, 2, 3, 4], 2], [[5, 1, 2, 3, 4], 3]],
#  [[[5, 1, 2, 3, 4], 3], [[5, 1, 2, 3, 4], 4]],
#  [[[5, 1, 2, 3, 4], 4], [[55, 55, 1, 2, 3, 4], 55]],
#  [[[55, 55, 1, 2, 3, 4], 55], [[55, 55, 1, 2, 3, 4], 55]],
#  [[[55, 55, 1, 2, 3, 4], 55], [[55, 55, 1, 2, 3, 4], 1]],
#  [[[55, 55, 1, 2, 3, 4], 1], [[55, 55, 1, 2, 3, 4], 2]],
#  [[[55, 55, 1, 2, 3, 4], 2], [[55, 55, 1, 2, 3, 4], 3]],
#  [[[55, 55, 1, 2, 3, 4], 3], [[55, 55, 1, 2, 3, 4], 4]]]


l // 3
# Out[3]:
# [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
#  [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31],
#  [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]]

for ini, v in enumerate(l.get_iter_random_values_from_iter_endless()):
    print(v)
    if ini == 5:
        break
# 36
# 34
# 15
# 23
# 17
# 32

l9 = NestedList(["abab", "cbcv", "banana", "bbb"])
l9.groupby_element_pos(1)
# Out[9]: {'b': ['abab', 'cbcv', 'bbb'], 'a': ['banana']}


l10 = NestedList(["aaabbb", "ccbbbb", "ab", "zcvcb", "abbab"])
l10.groupby_substring("abbb")
# Out[7]: {'abbb': ['aaabbb'], '': ['ccbbbb', 'zcvcb'], 'ab': ['ab'], 'abb': ['abbab']}

l11 = NestedList(
    [
        ["abab", "bac"],
        ["abab", "bac"],
        ["abab", "bac"],
        1,
        2,
        34,
        {43: 33},
        {43: 33},
    ]
)
l11.count_all_items()
# Out[11]: [(['abab', 'bac'], 3), (1, 1), (2, 1), (34, 1), ({43: 33}, 2)]


l12 = NestedList(["anton", "annabell", "anschalten"])
l12.find_common_start_string()
# Out[12]: 'an'


list(l.get_iter_item_difference())
# [1,
#  1,
#  1,
#  1,
#  1...

l2.index_all([4, 5, 6])
# Out[3]: [1]
l2.index_all([1, 2, 3])
# Out[4]: [0]

l13 = NestedList([1, 1, 2, 34, 4, 1, 1, 2, 34, 4, 1, 1])
l13.index_all(1)
# Out[6]: [0, 1, 5, 6, 10, 11]


l2.popleft()
# Out[5]: [1, 2, 3]
l2
# Out[6]: [[4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21]]


l2.appendleft(10)
l2
# Out[5]: [10, [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21]]


seq = (0, 1), (1, 1), (1, 0)
l13 = NestedList(
    [(random.randrange(0, 2), random.randrange(0, 2)) for _ in range(3000)]
)
for xz in l13.find_sequence(seq):
    print(xz)

l13.del_items((0, 0))

l.get_random_values_with_max_rep(10, 2)
# Out[4]: [29, 14, 47, 35, 11, 16, 26, 42, 40, 7]


l.get_random_not_repeating_values(10)
# Out[5]: [33, 37, 20, 14, 47, 17, 44, 2, 46, 32]


for key, item in (
    NestedList([[1, 2, 3, 4], [2, 3, 6]])
    .get_cycle_list_until_every_list_fits(
        maxresults=4,
        append=True,
    )
    .items()
):
    print(key, item)
# 12 defaultdict(<class 'list'>, {0: [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], 1: [[2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6]]})
# 24 defaultdict(<class 'list'>, {0: [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], 1: [[2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6]]})
# 36 defaultdict(<class 'list'>, {0: [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], 1: [[2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6]]})
# 48 defaultdict(<class 'list'>, {0: [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]], 1: [[2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6], [2, 3, 6]]})

l2.group_by(lambda x: isinstance(x, int))
# Out[6]:
# {True: [10],
#  False: [[4, 5, 6],
#   [7, 8, 9],
#   [10, 11, 12],
#   [13, 14, 15],
#   [16, 17, 18],
#   [19, 20, 21]]}


l.number_of_combinations(4)
# Out[10]: 230300


l3.flatten_and_group_by(lambda x: x > 10)
# Out[13]:
# {False: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#  True: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]}

l3.get_normalized_list_of_lists()
# Out[3]:
# [[[1, 2, 3], [4, 5, 6], None],
#  [[7, 8, 9], [10, 11, 12], None],
#  [[13, 14, 15], [16, 17, 18], [19, 20, 21]]]

list(l2[1:].get_iter_transposed_list_of_lists())
# Out[3]: [[4, 7, 10, 13, 16, 19], [5, 8, 11, 14, 17, 20], [6, 9, 12, 15, 18, 21]]


shu = l2.get_shuffle_copied_list()
print(shu)

for i, q in enumerate(
    l.get_iter_call_function_over_and_over_with_new_value(lambda x: [y * 2 for y in x])
):
    if i == 3:
        break
    print(q)
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41,
# 42, 43, 44, 45, 46, 47, 48, 49]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98]
# [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 148, 152, 156, 160, 164, 168, 172, 176, 180, 184, 188, 192, 196]


list(l[:10].get_iter_windowed_distance(fillvalue=None, distance=3))
# Out[9]:
# [(None, 0, 3),
#  (None, 1, 4),
#  (None, 2, 5),
#  (0, 3, 6),
#  (1, 4, 7),
#  (2, 5, 8),
#  (3, 6, 9),
#  (4, 7, None),
#  (5, 8, None),
#  (6, 9, None)]

list(l[:10].get_iter_2_cycle_second_until_first_done(range(3)))
# Out[11]:
# [(0, 0),
#  (1, 1),
#  (2, 2),
#  (3, 0),
#  (4, 1),
#  (5, 2),
#  (6, 0),
#  (7, 1),
#  (8, 2),
#  (9, 0)]


NestedList(
    [
        ("Maria", "Anna"),
        ("Anna", "Joao"),
        ("Kasimir", "Maria"),
        ("Hans", "Fritz"),
        ("Fritz", "Anna"),
        ("Günther", "Wolfgang"),
        ("Joao", "Wolfgang"),
    ]
).list_of_tuples_to_family_tree(main_mapping_keys=("Wolfgang",), bi_rl_lr="rl")

# ([(1, ('Wolfgang', 'Günther')),
#   (2, ('Wolfgang', 'Joao', 'Anna', 'Maria', 'Kasimir')),
#   (3, ('Wolfgang', 'Joao', 'Anna', 'Fritz', 'Hans'))],
#  {'Wolfgang': {'Günther': 1,
#    'Joao': {'Anna': {'Maria': {'Kasimir': 2}, 'Fritz': {'Hans': 3}}}}})


NestedList(["ababa", "bubax", "ali bbaba"]).get_levenshtein_distance("ali baba")
# Out[3]: [[(1, 2, 'ali bbaba', 'ali baba'), (3, 0, 'ababa', 'ali baba'), (6, 1, 'bubax', 'ali baba')]]


NestedList(
    [
        [[("Maria", "Anna"), ("Anna", "Joao")]],
        {("Kasimir", "Maria"), ("Hans", "Fritz")},
        ("Fritz", "Anna"),
        {"Günther": "Wolfgang"},
        ("Joao", "Wolfgang"),
    ]
).flatten_level(n=None, dict_treatment="items", consider_non_iter=(str, bytes, dict))
# Out[5]:
# ['Maria',
#  'Anna',
#  'Anna',
#  'Joao',
#  'Kasimir',
#  'Maria',
#  'Hans',
#  'Fritz',
#  'Fritz',
#  'Anna',
#  {'Günther': 'Wolfgang'},
#  'Joao',
#  'Wolfgang']

print(l.group_sequences(fu=lambda a, b: b > a)[0])
p = NestedList(["a", "aa", "b", "bbb", "c", "d", "dd", "ddd", "vbvdddd"])

print(p.group_sequences(fu=lambda a, b: a in b))
# [['a', 'aa'], ['b', 'bbb'], ['c'], ['d', 'dd', 'ddd', 'vbvdddd']]

k = NestedList([random.randint(0, 5) for x in range(20)])
print(k.group_sequences(lambda a, b: b >= a))
# [3, 1, 3, 5, 3, 4, 4, 3, 4, 3, 4, 4, 5, 1, 3, 2, 3, 1, 1, 3]
# [[3], [1, 3, 5], [3, 4, 4], [3, 4], [3, 4, 4, 5], [1, 3], [2, 3], [1, 1, 3]]


o = NestedList(
    [(1, 2), (3, 4), (501, 641), (300, 4500), (1, 4344)]
).groupby_euclid_dist(
    coord=(0, 0),
    mindistance=0,
    maxdistance=500,
)
# Out[6]: {True: [(1, 2), (3, 4)], False: [(501, 641), (300, 4500), (1, 4344)]}


NestedList(["a", "bbb", "b", "ddd", "444444"]).groupby_string_length()
# Out[3]: {1: ['a', 'b'], 3: ['bbb', 'ddd'], 6: ['444444']}


NestedList(
    ["a", "bbb", "b", "ddd", "444444", [1, [1, 1, 1, 1, 1, 1, [1]]]]
).group_values_in_flattened_nested_iter_and_count()
# Out[4]: {'a': 1, 'bbb': 1, 'b': 1, 'ddd': 1, '444444': 1, 1: 8}


NestedList(
    ["a", "bbb", "b", "ddd", "444444", [1, [1, 1, 1, 1, 1, 1, [1]]]]
).groupby_type()
# Out[5]: {str: ['a', 'bbb', 'b', 'ddd', '444444'], list: [[1, [1, 1, 1, 1, 1, 1, [1]]]]}


NestedList(
    ["a", "bbb", "b", "ddd", "444444", "a", "a", "ddd", [1, [1, 1, 1, 1, 1, 1, [1]]]]
).groupby_frequency()
# Out[6]:
# {3: ['a', 'a', 'a'],
#  1: ['bbb', 'b', '444444', [1, [1, 1, 1, 1, 1, 1, [1]]]],
#  2: ['ddd', 'ddd']}

NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_can_be_divided_by(2)
# Out[7]: {True: [4, 2, 2, 2344, 444, 222, 8, 0], False: [7, 7, 9, 7, 65, 45]}

NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_division_remainder(2)
# Out[8]: {0: [4, 2, 2, 2344, 444, 222, 8, 0], 1: [7, 7, 9, 7, 65, 45]}

NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_divisor(2)
# Out[9]:
# {2: [4],
#  1: [2, 2],
#  1172: [2344],
#  222: [444],
#  111: [222],
#  3: [7, 7, 7],
#  4: [8, 9],
#  0: [0],
#  32: [65],
#  22: [45]}

NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_bigger_than_or_equal(100)
# Out[10]: {False: [4, 2, 2, 7, 7, 8, 9, 0, 7, 65, 45], True: [2344, 444, 222]}

NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_less_than_or_equal(100)
# Out[11]: {True: [4, 2, 2, 7, 7, 8, 9, 0, 7, 65, 45], False: [2344, 444, 222]}


NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_bigger_than(100)
# Out[12]: {False: [4, 2, 2, 7, 7, 8, 9, 0, 7, 65, 45], True: [2344, 444, 222]}
NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_less_than(100)
# Out[13]: {True: [4, 2, 2, 7, 7, 8, 9, 0, 7, 65, 45], False: [2344, 444, 222]}

NestedList(
    [
        4,
        2,
        2,
        2344,
        444,
        222,
        7,
        7,
        8,
        9,
        0,
        7,
        65,
        45,
    ]
).groupby_equal(7)
# Out[14]: {False: [4, 2, 2, 2344, 444, 222, 8, 9, 0, 65, 45], True: [7, 7, 7]}

NestedList(
    ["1342423", "ddd", "33333", "ixxx", "00"]
).groupby_regular_expression_matches(r"\d+")
# Out[15]: {True: ['1342423', '33333', '00'], False: ['ddd', 'ixxx']}

NestedList([2.0, 1, 1, 3, 5, 3.0, 3.4, 2.4, 25.3]).groupby_is_integer()
# Out[17]: {True: [2.0, 1, 1, 3, 5, 3.0], False: [3.4, 2.4, 25.3]}

NestedList(
    [1.0, 1.1, 1.2, 1.3, 1.9, 1.8, 2.0, 1, 1, 3, 5, 3.0, 3.4, 2.4, 25.3]
).groupby_floor()
# Out[18]:
# {1: [1.0, 1.1, 1.2, 1.3, 1.9, 1.8, 1, 1],
#  2: [2.0, 2.4],
#  3: [3, 3.0, 3.4],
#  5: [5],
#  25: [25.3]}
NestedList(
    [1.0, 1.1, 1.2, 1.3, 1.9, 1.8, 2.0, 1, 1, 3, 5, 3.0, 3.4, 2.4, 25.3]
).groupby_ceil()
# Out[19]:
# {1: [1.0, 1, 1],
#  2: [1.1, 1.2, 1.3, 1.9, 1.8, 2.0],
#  3: [3, 3.0, 2.4],
#  5: [5],
#  4: [3.4],
#  26: [25.3]}

seq = [
    1.11111111,
    1.111222222,
    1.11113334,
    1.3,
    1.9,
    1.8,
    2.0,
    1,
    1,
    3,
    5,
    3.0,
    3.4,
    2.4,
    25.3,
]
NestedList(seq).groupby_round(n=2)
# Out[21]:
# {1.11: [1.11111111, 1.111222222, 1.11113334],
#  1.3: [1.3],
#  1.9: [1.9],
#  1.8: [1.8],
#  2.0: [2.0],
#  1: [1, 1],
#  3: [3, 3.0],
#  5: [5],
#  3.4: [3.4],
#  2.4: [2.4],
#  25.3: [25.3]}

seq = ["hallo", "boot", "baba", "bdoo", "flaot", "mama"]
NestedList(seq).groupby_endswith(n=1)
# Out[22]: {'o': ['hallo', 'bdoo'], 't': ['boot', 'flaot'], 'a': ['baba', 'mama']}


NestedList(seq).groupby_startswith(n=1)
# Out[23]: {'h': ['hallo', 'hmama'], 'b': ['boot', 'baba', 'bdoo'], 'f': ['flaot']}


NestedList(seq).groupby_first_occurrence_in_string(char="a")
# Out[25]: {1: ['hallo', 'baba'], -1: ['boot', 'bdoo'], 2: ['flaot', 'hmama']}

NestedList(seq).groupby_last_occurrence_in_string(char="a")
# Out[26]: {1: ['hallo'], -1: ['boot', 'bdoo'], 3: ['baba'], 2: ['flaot'], 4: ['hmama']}

NestedList(seq).groupby_isalnum()
# Out[28]: {True: ['One', '222'], False: ['%', '#']}

NestedList(seq).groupby_isalpha()
# Out[29]: {True: ['One'], False: ['%', '#', '222']}

NestedList(seq).groupby_isascii()
# Out[31]: {True: ['One', '%', '#', '222'], False: ['ç', 'ß']}

NestedList(seq).groupby_isdecimal()
# Out[32]: {False: ['One', '%', '#', 'ç', 'ß'], True: ['222']}

seq = """One % # 222 ç ß""".split()
NestedList(seq).groupby_isdigit()
# Out[33]: {False: ['One', '%', '#', 'ç', 'ß'], True: ['222']}

seq = """One % # 222 ç ß True if bool""".split()
NestedList(seq).groupby_isidentifier()
# Out[35]: {True: ['One', 'ç', 'ß', 'True', 'if', 'bool'], False: ['%', '#', '222']}

seq = """One % # 222 ç ß True if bool""".split()
NestedList(seq).groupby_islower()
# Out[37]: {False: ['One', '%', '#', '222', 'True'], True: ['ç', 'ß', 'if', 'bool']}

NestedList(seq).groupby_isnumeric()
# Out[38]: {False: ['One', '%', '#', 'ç', 'ß', 'True', 'if', 'bool'], True: ['222']}

seq = """One % # 222 ç ß True if bool""".split() + ["\r"]
NestedList(seq).groupby_isprintable()
# Out[42]: {True: ['One', '%', '#', '222', 'ç', 'ß', 'True', 'if', 'bool'], False: ['\r']}

NestedList(seq).groupby_isspace()
# Out[43]: {False: ['One', '%', '#', '222', 'ç', 'ß', 'True', 'if', 'bool'], True: ['\r']}

NestedList(seq).groupby_istitle()
# Out[44]: {True: ['One', 'True'], False: ['%', '#', '222', 'ç', 'ß', 'if', 'bool', '\r']}


seq = """One % # 222 ç ß True if bool AA""".split() + ["\r"]
NestedList(seq).groupby_isupper()
# Out[46]:
# {False: ['One', '%', '#', '222', 'ç', 'ß', 'True', 'if', 'bool', '\r'],
#  True: ['AA']}

seq = """One % # 222 ç ß True if bool AA""".split()
NestedList(seq).groupby_isin("e")
# Out[48]: {True: ['One', 'True'], False: ['%', '#', '222', 'ç', 'ß', 'if', 'bool', 'AA']}

seq = [
    (
        g := random.randrange(1, 200),
        f := random.randrange(1, 200),
        g + 100,
        f + 100,
    )
    for _ in range(10)
]


import numpy as np
import pandas as pd

seq = [pd.NA, np.nan, None, math.nan, 3, 54, 3, (22, 34, 412), {323, 31}, [3312, 3]]
NestedList(seq).groupby_isna(
    emptyiters=False,
    nastrings=False,
    emptystrings=False,
    emptybytes=False,
    continue_on_exceptions=True,
    withindex=False,
    withvalue=True,
)
# Out[4]:
# {True: [<NA>, nan, None, nan],
#  False: [3, 54, 3, (22, 34, 412), {31, 323}, [3312, 3]]}


seq = [pd.NA, np.nan, None, math.nan, 3, 54, 3, (22, 34, 412), {323, 31}, [3312, 3]]
NestedList(seq).groupby_isiter()
# Out[5]:
# {False: [<NA>, nan, None, nan, 3, 54, 3],
#  True: [(22, 34, 412), {31, 323}, [3312, 3]]}


import os

NestedList(os.listdir(r"F:\gitrep\screenshots")).groupby_file_extension()


seq = [1, 2, 3, 45, 56, 6, 32, 12]
NestedList(seq).groupby_even_odd()
# Out[7]: {'odd': [1, 3, 45], 'even': [2, 56, 6, 32, 12]}

seq = [
    os.path.join(r"F:\gitrep\screenshots", x)
    for x in os.listdir(r"F:\gitrep\screenshots")
]

NestedList(seq).groupby_files_folder_link()

seq = [
    [
        1,
        2,
        34,
    ],
    (1, 32, 4),
    (2, 3, 4, 54),
    [2, 3, 3],
]
NestedList(seq).groupby_first_item()
# Out[11]: {1: [[1, 2, 34], (1, 32, 4)], 2: [(2, 3, 4, 54), [2, 3, 3]]}


NestedList(
    ["autobahn", "computerproblem", "kind", "opa", "kind opa"]
).groupby_words_in_texts(
    wordlist=["kind", "opa"],
    case_sen=False,
    continue_on_exceptions=True,
    withindex=False,
    boundary_right=True,
    boundary_left=True,
)
# Out[4]:
# {(): ['autobahn', 'computerproblem'],
#  ('kind',): ['kind'],
#  ('opa',): ['opa'],
#  ('kind', 'opa'): ['kind opa']}


seq = [[1, 2, 2], [5], [2, 3], [4, 4, 4], [12, 0], [6, 6], [1, 2]]
NestedList(seq).groupby_sum()
# Out[5]: {5: [[1, 2, 2], [5], [2, 3]], 12: [[4, 4, 4], [12, 0], [6, 6]], 3: [[1, 2]]}

seq = ["https://www.google.com", "google.com/", "bababa", "http://baba.de"]
NestedList(seq).groupby_valid_url()
# Out[6]:
# {'valid': ['https://www.google.com', 'http://baba.de'],
#  'not_valid': ['google.com/', 'bababa']}


seq = ["11", "bb", '"bb"']
NestedList(seq).groupby_literal_eval_type()
# Out[7]:
# {int: ['11'],
#  'EXCEPTION: malformed node or string on line 1: <ast.Name object at 0x000001BE3C6AC0A0>': ['bb'],
#  str: ['"bb"']}


seq = [b"\\U0001D11E", b"baba"]
NestedList(seq).groupby_decoding_result()


seq = 2 * [1, 2, 34, 4, 2, 3, 54, 6, 6, 4, 3, 2, 21, 45, 56]
NestedList(seq).groupby_percentage(percent_true=63.7)
# Out[4]:
# {True: [1, 34, 2, 3, 54, 6, 2, 21, 45, 56, 1, 34, 4, 2, 3, 6, 4, 3, 2, 45, 56],
#  False: [2, 4, 6, 4, 3, 2, 54, 6, 21]}


seq = [11, 200, 34, 4, 52, 63, 54, 65, 67, 48, 3, 2, 21, 55, 56, 59, 61, 60]
NestedList(seq).groupby_almost_equal(value=60, equallimit=3)
# Out[6]:
# {False: [11, 200, 34, 4, 52, 54, 65, 67, 48, 3, 2, 21, 55, 56],
#  True: [63, 59, 61, 60]}

seq = 2 * [(1, 2), (34, 4), (2, 3), (61, 60)]
NestedList(seq).groupby_coords_almost_equal(
    x_coord=4,
    y_coord=3,
    limit_x=5,
    limit_y=1,
)
# Out[7]:
# {(True, True): [(1, 2), (2, 3), (1, 2), (2, 3)],
#  (False, True): [(34, 4), (34, 4)],
#  (False, False): [(61, 60), (61, 60)]}


coordlist = [
    (745, 519),
    (747, 522),
    (747, 517),
    (747, 517),
    (750, 522),
    (756, 449),
    (757, 461),
    (757, 461),
    (757, 438),
    (830, 144),
    (759, 435),
    (759, 435),
    (761, 468),
    (761, 468),
    (764, 521),
    (1079, 199),
    (770, 474),
    (770, 425),
    (773, 516),
    (776, 515),
    (776, 515),
    (778, 520),
    (779, 519),
    (780, 420),
    (780, 420),
    (782, 478),
    (782, 478),
    (1083, 151),
    (1083, 151),
    (1083, 151),
    (1083, 151),
    (784, 478),
    (759, 435),
    (784, 478),
    (819, 137),
    (819, 137),
    (819, 137),
    (797, 524),
    (825, 125),
    (826, 149),
    (800, 446),
    (800, 446),
    (801, 517),
    (801, 517),
    (802, 520),
    (802, 520),
    (804, 519),
    (804, 519),
    (808, 431),
    (808, 431),
    (809, 464),
    (809, 464),
    (812, 438),
    (813, 449),
]
xx = NestedList(coordlist).group_coordinates_by_distance(
    coordlist, limit_x=10, limit_y=10, continue_on_exceptions=True
)
for x in xx:
    print(x)
#
# ((813, 449),)
# ((779, 519), (773, 516), (776, 515), (778, 520), (764, 521))
# ((808, 431), (812, 438))
# ((1083, 151),)
# ((830, 144), (826, 149))
# ((761, 468), (757, 461), (770, 474))
# ((825, 125),)
# ((756, 449),)
# ((745, 519), (747, 517), (750, 522), (747, 522))
# ((780, 420), (770, 425))
# ((784, 478), (782, 478))
# ((804, 519), (802, 520), (797, 524), (801, 517))
# ((757, 438), (759, 435))
# ((819, 137),)
# ((809, 464),)
# ((800, 446),)
# ((1079, 199),)


seq = sorted(list(range(0, 5)) * 3)
print(NestedList(seq).bisect_rightmost_value_equal_to(4))
print(NestedList(seq).bisect_rightmost_value_equal_to(0))
print(NestedList(seq).bisect_rightmost_value_equal_to(1))
print(NestedList(seq).bisect_leftmost_value_equal_to(4))
print(NestedList(seq).bisect_leftmost_value_equal_to(0))
print(NestedList(seq).bisect_leftmost_value_equal_to(1))
print(NestedList(seq).bisect_rightmost_value_less_than(4))
print(NestedList(seq).bisect_rightmost_value_less_than(2))
print(NestedList(seq).bisect_rightmost_value_less_than(1))
print(NestedList(seq).bisect_rightmost_value_less_than_or_equal(40))
print(NestedList(seq).bisect_rightmost_value_less_than_or_equal(0))
print(NestedList(seq).bisect_rightmost_value_less_than_or_equal(1))
print(NestedList(seq).bisect_leftmost_value_greater_than(2))
print(NestedList(seq).bisect_leftmost_value_greater_than(3))
print(NestedList(seq).bisect_leftmost_value_greater_than(0))
print(NestedList(seq).bisect_leftmost_value_greater_than(1))
print(NestedList(seq).bisect_leftmost_value_greater_than_or_equal(3))
print(NestedList(seq).bisect_leftmost_value_greater_than_or_equal(0))
print(NestedList(seq).bisect_leftmost_value_greater_than_or_equal(1))

# 14
# 2
# 5
# 12
# 0
# 3
# 11
# 5
# 2
# 14
# 2
# 5
# 9
# 12
# 3
# 6
# 9
# 0
# 3


cervejas = [
    ("original", 2.5),
    ("Skol", 0.5),
    ("becks", 16),
    ("brahma", 1.4),
    ("heineken", 5.5),
]
cats_ = [
    ("barato", 1.3),
    ("mais ou menos", 2),
    ("caro", 3.1),
    ("muito caro", 6.5),
    ("absurdo", sys.maxsize),
]
NestedList(cervejas).bisect_category_mapping(cats_)
# Out[4]:
# [(('original', 2.5), 'caro'),
#  (('Skol', 0.5), 'barato'),
#  (('becks', 16), 'absurdo'),
#  (('brahma', 1.4), 'mais ou menos'),
#  (('heineken', 5.5), 'muito caro')]


text = """
Read the running tests and linters section of our documentation to learn how to test your code. For cross-browser
""".split() + [
    1,
    2,
    3,
]
list(
    NestedList(text).get_iter_list_ljust_rjust(
        ljust=None,  # if None and getmax is True -> the longest str will be used
        ljustchr="-",  # fill with char
        rjust=None,  # if None and getmax is True -> the longest str will be used
        rjustchr="-",  # fill with char
        getmax=True,
    )
)
# Out[5]:
# ['---------Read',
#  '----------the',
#  '------running',
#  '--------tests',
#  '----------and',
#  '------linters',
#  '------section',
#  '-----------of',
#  '----------our',
#  'documentation',
#  '-----------to',
#  '--------learn',
#  '----------how',
#  '-----------to',
#  '---------test',
#  '---------your',
#  '--------code.',
#  '----------For',
#  'cross-browser',
#  '------------1',
#  '------------2',
#  '------------3']

for li in NestedList((list(range(20)))).get_iter_log_split():
    print(li)

# [0]
# [1, 2]
# [3, 4, 5]
# [6, 7, 8, 9]
# [10, 11, 12, 13, 14]
# [15, 16, 17, 18, 19]

  ```