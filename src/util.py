from defines import *

def thr_indice(index) :
    for i in xrange(num_thread_region) :
        yield to_global_thr_index(index, i)

def to_global_thr_index(index, thr_index) :

    proc_col = index % num_region_x
    proc_row = index / num_region_x
    
    thr_col = thr_index % num_thread_region_x
    thr_row = thr_index / num_thread_region_x

    # print  '((%s + (%s * %s + %s) * %s) * %s + %s)' % (proc_col, proc_row, num_thread_region_y, thr_row, num_region_x, num_thread_region_x, thr_col)

    return ((proc_col + (proc_row * num_thread_region_y + thr_row) * num_region_x) * num_thread_region_x + thr_col)
    

def one_2_two(index, num_x, total_x, num_y, total_y) :
    num_per_x = total_x / num_x
    num_per_y = total_y / num_y
    x = temp_x = (index % num_x) * num_per_x
    y = temp_y = (index / num_x) * num_per_y

    while y < temp_y + num_per_y :
        x = temp_x
        while x < temp_x + num_per_x :
            yield (x, y)
            x += 1
        y += 1

def cells_of_region(index) :
    return one_2_two(index, num_region_x, num_cell_x, num_region_y, num_cell_y)

def cells_of_thread(index) :
    return one_2_two(index, num_region_x * num_thread_region_x, num_cell_x, num_region_y * num_thread_region_y, num_cell_y)
