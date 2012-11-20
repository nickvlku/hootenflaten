from flask import current_app

import time

__author__ = 'nick'

@current_app.template_filter('epoch')
def epoch_time(d):
    return int(time.mktime(d.timetuple()))

