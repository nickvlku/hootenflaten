# -*- coding: utf-8 -*-

__author__ = 'nick'

from flask import current_app
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger)
