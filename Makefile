SRC_DIR = src
DATA_DIR = data

all: 

data:
	mkdir $(DATA_DIR)
	python $(SRC_DIR)/data.py $(DATA_DIR)

rmdata:
	rm -rf $(DATA_DIR)

clean:
	rm -rf .*~
	rm -rf $(SRC_DIR)/*~
	rm -rf $(SRC_DIR)/*.pyc
