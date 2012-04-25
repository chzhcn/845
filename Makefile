SRC_DIR = src
DATA_DIR = /afs/andrew.cmu.edu/usr16/hsuehhac/public/data

all: 

.PHONY : data
data:
	mkdir -p $(DATA_DIR)
	python $(SRC_DIR)/data.py $(DATA_DIR)

dc:
	python $(SRC_DIR)/disaster_controller.py $(DATA_DIR)

lis:
	python $(SRC_DIR)/listen_sys.py

mon:
	python $(SRC_DIR)/mon_sys.py $(DATA_DIR)

rmdata:
	rm -rf $(DATA_DIR)

clean:
	rm -rf .*~
	rm -rf $(SRC_DIR)/*~
	rm -rf $(SRC_DIR)/*.pyc
