import appdaemon.plugins.hass.hassapi as hass

#
# App to turn something on when a sensor is activated.
#
# Use with constrints to activate only for the hours of darkness
#
# Args:
# sensor: binary sensor to use as trigger
# entity : entity to turn on when sensor is detected, can be a light, script, scene or anything else that can respond to homeassistant.turn_on
#
# Release Notes
#
# Version 1.1:
#   Add ability for other apps to cancel the timer
#
# Version 1.0:
#   Initial Version

class OccupancyActivate(hass.Hass):

    def initialize(self):
        self.handle = None
        # Check some Params
        # Subscribe to sensors
        if "sensor" in self.args:
            if "entity" in self.args:
                self.log("Registering 'on' listener for %s, activates %s"
                        % (self.args["sensor"], self.args["entity"]))
                self.listen_state(self.activated, self.args["sensor"], new="on")
            else:
                self.log("No activation target specified for sensor, doing nothing.")
        else:
            self.log("No sensor specified, doing nothing")
    
    def activated(self, entity, attribute, old, new, kwargs):
        self.log("Sendor activated: turning {} on".format(self.args["entity"]))
        self.turn_on(self.args["entity"])
