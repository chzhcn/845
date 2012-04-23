# cell is a tract
# region is a server zone

total_server = 48000000

num_cell_x = 800
num_cell_y = 300

num_region_x = 8
num_region_y = 4

sample_rate = 0.1

server_per_cell = total_server / (num_cell_x * num_cell_y)

num_region = num_region_x * num_region_y

num_cell = num_cell_x * num_cell_y

cell_per_region_x = num_cell_x / num_region_x
cell_per_region_y = num_cell_y / num_region_y

num_thread_region_x = 4
num_thread_region_y = 3

num_thread_region = (num_thread_region_x * num_thread_region_y)
