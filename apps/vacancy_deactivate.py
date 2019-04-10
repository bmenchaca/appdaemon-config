import appdaemon.plugins.hass.hassapi as hass

#
# App to turn things off after a binary sensor has been off for a while.
#
# Use with constrints to activate only for the hours of darkness
#
# Args:
# sensor: binary sensor to use as trigger
# delay: time in seconds after sensor stays off to declare vacancy.  If not specified there is 0 delay.
# entity: entity to turn off when sensor has been off for <delay> seconds.  This can be anything that
#     homeassistant.turn_off can turn off.  Must have this entry, or scene. This entity won't work with
#     scenes.
# scene: scene to turn on when the sensor has been off for <delay> seconds.  Must have this entry, or
#    entity.  This entry only works with scenes.
#
# Release Notes
#
# Version 1.0:
#   Initial Version

class VacancyDeactivate(hass.Hass):
    def initialize(self):
        self.handle = None
        # Check some Params
        # Subscribe to sensors
        if "sensor" in self.args:
            if "delay" in self.args:
                delay = self.args["delay"]
            else:
                delay = 0
            if "entity" in self.args:
                self.log("Registering off listener for %s quiesce, turns off entity %s after %d seconds." % (self.args["sensor"], self.args["entity"], delay))
                self.listen_state(self.quiesce_for_entity, self.args["sensor"], new='off', duration=delay)
            elif "scene" in self.args:
                self.log("Registering off listener for %s quiesce, turns on scene %s after %d seconds." % (self.args["sensor"], self.args["scene"], delay))
                self.listen_state(self.quiesce_for_scene, self.args["sensor"], new='off', duration=delay)
            else:
                self.log("Nothing to change when vacancy is detected.  Please specify a deactivated_entity or a deactivation_scene.")
        else:
            self.log("No sensor specified, doing nothing")
    

    def quiesce_for_scene(self, entity, attribute, old, new, kwargs):
        self.log("Motion stopped: turning scene {} on".format(self.args["scene"]))
        self.turn_on(self.args["scene"])
  

    def quiesce_for_entity(self, entity, attribute, old, new, kwargs):
        self.log("Motion stopped: turning entity {} off".format(self.args["entity"]))
        self.turn_off(self.args["entity"])
