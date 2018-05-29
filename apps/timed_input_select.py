import datetime
import time
import appdaemon.plugins.hass.hassapi as hass

#
# App to advance an input select through various states as the day progresses.
#
# Add constraints to only do particular days of the week.
#
# Args:
#
# selector: The input selector to change
# schedule: A dictionary with the selector entries as keys, and the (H, M, S) specification as values.
#
# Version 1.0:
#   Initial Version

class TimedInputSelect(hass.Hass):

    def initialize(self):
        # Check some Params
        # Subscribe
        if not "selector" in self.args:
            self.log("No selector specified, doing nothing.")
            return
        if not "schedule" in self.args or not self.args["schedule"]:
            self.log("No schedule specified, doing nothing.")
            return

        for (selector_key, hms) in self.args["schedule"].items():
            time_struct = datetime.datetime.strptime(hms, '%H:%M:%S').time()
            self.log("Setting timer to change to %s at %s each day" % (selector_key, time_struct))
            self.run_daily(self.advance_selector, time_struct,
                           selector=self.args["selector"], key=selector_key)

        # Also, listen for HA to restart so we can re-set the selector
        self.listen_event(self.ha_event, "plugin_started")
    

    def advance_selector(self, kwargs):
        self.select_option(kwargs["selector"], kwargs["key"])

    def ha_event(self, event_name, data, kwargs):
        self.log("HA restart detected, finding correct time of day.")
        schedule_list = []
        for (selector_key, hms) in self.args["schedule"].items():
            dt = datetime.datetime.strptime(hms, '%H:%M:%S').time()
            schedule_list.append((selector_key, dt))
        sorted_list = sorted(schedule_list, key=lambda p: p[1])
        self.log("List of times: %s." % sorted_list)
        current = datetime.datetime.now().time()
        selected = sorted_list[-1][0];
        for (key, hms) in sorted_list:
            if current < hms:
                self.select_option(self.args["selector"], selected)
                self.log("Selected %s since current time %s is less than %s." %
                         (selected, current, hms))
                return
            else:
                selected = key
        self.select_option(kwargs["selector"], selected)
        self.log("Selecting last entry %s since current time %s is greater than last time %s." % (selected, current, sorted_list[-1][1]))

