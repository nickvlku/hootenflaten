from base import app

import time

__author__ = 'nick'

@app.template_filter('epoch')
def epoch_time(d):
    return int(time.mktime(d.timetuple()))

