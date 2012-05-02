from defines_one import *

num_sample = 17

success_threshold = 0.4

server_per_cell = total_server / (num_cell_x * num_cell_y)
num_region = num_region_x * num_region_y

num_cell = num_cell_x * num_cell_y

cell_per_region_x = num_cell_x / num_region_x
cell_per_region_y = num_cell_y / num_region_y

num_thread_region = (num_thread_region_x * num_thread_region_y)

report_addr = ('127.0.0.1', 54321)

normal_prob = 0.90

num_collect = 1000
