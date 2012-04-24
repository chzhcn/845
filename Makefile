SRC_DIR = src
DATA_DIR = /afs/andrew.cmu.edu/usr18/chiz/Public/data

all: 

data:
	mkdir -p $(DATA_DIR)
	python $(SRC_DIR)/data.py $(DATA_DIR)

mon:
	python $(SRC_DIR)/mon_sys.py $(DATA_DIR)

rmdata:
	rm -rf $(DATA_DIR)

clean:
	rm -rf .*~
	rm -rf $(SRC_DIR)/*~
	rm -rf $(SRC_DIR)/*.pyc
