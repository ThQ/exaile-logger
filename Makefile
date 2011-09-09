ROOT_DIR:= $(shell pwd)
PLUGIN_NAME:=logger
BUILD_DIR:=${ROOT_DIR}/build
BUILD_LOGGER_DIR:=$(BUILD_DIR)/$(PLUGIN_NAME)
SRC_DIR:=${ROOT_DIR}/src
EXZ_FILE:=$(BUILD_DIR)/$(PLUGIN_NAME).exz

exz: build_dir
	if [ ! -d "$(BUILD_LOGGER_DIR)" ] ; then mkdir -p $(BUILD_LOGGER_DIR) ; fi
	find $(SRC_DIR)/ -iname "*.pyc" -exec rm {} \;
	cp -a $(SRC_DIR)/* $(BUILD_DIR)
	cd $(BUILD_DIR) && tar -cvf $(EXZ_FILE) $(PLUGIN_NAME) ; cd $(ROOT_DIR)

build_dir:
	if [ ! -d $(BUILD_DIR) ] ; then mkdir $(BUILD_DIR) ; fi
	rm -rf $(BUILD_DIR)/*
