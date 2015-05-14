WORKFLOW := "ALS\ Typograf.alfredworkflow"
SRC_DIR := alfred-typograf
SRC := info.plist typograf.py icon.png
VPATH := $(SRC_DIR) 

all: $(WORKFLOW)

$(WORKFLOW): $(SRC)
	cd $(SRC_DIR) && zip $@ $(^F) && mv $@ ..

install: $(WORKFLOW)
	open $<
