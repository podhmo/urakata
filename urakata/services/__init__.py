# -*- coding:utf-8 -*-
from .registration import get_registration
from .admindo import get_admindo
from .addscaffold import get_addscaffold
from .codegen import get_codegen
from ..interfaces import IScanConfig


def get_scan_config(request, root):
    return request.find_service(IScanConfig)(request, root)

__all__ = [
    "get_registration",
    "get_admindo",
    "get_addscaffold",
    "get_codegen"
]
