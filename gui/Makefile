
PYUIC=pyuic5
PFLAGS=

GREEN=ui/green/SingleEnergyPitchIJ_design.py ui/green/BeamsizeMeasurement_design.py ui/green/r12_design.py

all: ui/detcal_design.py ui/distfunc_anapitch_design.py ui/distfunc_design.py ui/image_design.py ui/meq_design.py ui/orbits_design.py ui/sightlineMappings_design.py ui/sightlineMappingsView_design.py $(GREEN)

ui/%_design.py: ui/%.ui
	$(PYUIC) $(PFLAGS) $< -o $@

ui/green/%_design.py: ui/green/%.ui
	$(PYUIC) $(PFLAGS) $< -o $@

clean:
	rm ui/*.py
	rm ui/green/*.py

