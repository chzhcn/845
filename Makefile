SRC_DIR = src
DATA_DIR = data

all: 

data:
	mkdir -p $(DATA_DIR)
	python $(SRC_DIR)/data.py $(DATA_DIR)

run: lis mon

lis:
	python $(SRC_DIR)/listen_sys.py $
mon:
	python $(SRC_DIR)/mon_sys.py $(DATA_DIR)

rmdata:
	rm -rf $(DATA_DIR)

clean:
	rm -rf .*~
	rm -rf $(SRC_DIR)/*~
	rm -rf $(SRC_DIR)/*.pyc
