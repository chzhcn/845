from defines_small import *

sample_rate = 0.1

success_threshold = 0.5

server_per_cell = total_server / (num_cell_x * num_cell_y)

num_region = num_region_x * num_region_y

num_cell = num_cell_x * num_cell_y

cell_per_region_x = num_cell_x / num_region_x
cell_per_region_y = num_cell_y / num_region_y

num_thread_region = (num_thread_region_x * num_thread_region_y)

report_addr = ('128.2.13.133', 54321)
