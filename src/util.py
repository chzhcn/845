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
    temp_x = (index % num_x) * num_per_x
    temp_y = (index / num_x) * num_per_y

    for y in xrange(temp_y, temp_y + num_per_y) :
        x = temp_x
        for x in xrange(temp_x, temp_x + num_per_x) :
            yield (y, x)        # in form of (y, x), which is (row, column)

def region_index_2_grid(index) :
    temp = [grid for grid in one_2_two(index, num_region_x, num_region_x, num_region_y, num_region_y)]
    assert (len(temp) == 1)
    return temp[0]

def region_grids_with_corner_indice(topleft, bottomright) :
    tl = region_index_2_grid(topleft)
    bt = region_index_2_grid(bottomright)

    for y in xrange(tl[0], bt[0] + 1) :
        x = tl[0]
        for x in xrange (tl[1], bt[1] + 1) :
            yield y*num_region_x + x

def cell_to_region(cell):
    row,col = cell
    reg_row = row / cell_per_region_y
    reg_col = col / cell_per_region_x
    region_index = reg_row*num_region_x + reg_col
    return region_index

def cells_of_region(index) :
    return one_2_two(index, num_region_x, num_cell_x, num_region_y, num_cell_y)

def cells_of_thread(index) :
    return one_2_two(index, num_region_x * num_thread_region_x, num_cell_x, num_region_y * num_thread_region_y, num_cell_y)
