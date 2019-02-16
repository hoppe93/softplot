
PYUIC=pyuic5
PFLAGS=

all: ui/image_design.py ui/meq_design.py

ui/%_design.py: ui/%.ui
	$(PYUIC) $(PFLAGS) $< -o $@

clean:
	rm ui/*.py
