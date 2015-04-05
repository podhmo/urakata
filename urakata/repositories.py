# -*- coding:utf-8 -*-
from .models import (
    Session,
    Scaffold,
    ScaffoldHistory
)


class ScaffoldRepository(object):
    def __init__(self, request):
        self.request = request

    def get(self, name, version=None):
        classes = [Scaffold, ScaffoldHistory]
        for m in classes:
            qs = Session.query(m).filter(m.name == name)
            if version:
                qs = qs.filter(m.version == version)
            ob = qs.first()
            if ob:
                return ob
