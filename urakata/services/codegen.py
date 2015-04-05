# -*- coding:utf-8 -*-
import inspect
from prestring.python import PythonModule
from urakata.decorator import reify
from urakata.emitter import InputWrapper


class CodeGenerator(object):
    def __init__(self, request):
        self.request = request
        self.m = PythonModule()
        self.toplevel = self.m.submodule()

    def get_source_code(self, ob):
        return inspect.getsource(ob.__class__)

    def build_main(self, scaffold):
        pass

    def codegen(self, scaffold, emitter):
        self.m.stmt(self.get_source_code(emitter))
        self.m.stmt(self.get_source_code(emitter.env))
        self.m.stmt(self.get_source_code(emitter.config))
        self.m.stmt(self.get_source_code(emitter.config.name_scanner))
        self.m.stmt(self.get_source_code(emitter.config.template_scanner))

        # module
        self.toplevel.import_("sys")
        self.toplevel.import_("os.path")
        self.toplevel.import_("re")
        self.toplevel.from_("collections", "defaultdict")
        self.toplevel.from_("collections", "Mapping")
        self.toplevel.from_("collections", "OrderedDict")
        self.toplevel.import_("logging")
        self.toplevel.stmt("logger = logging.getLogger(__name__)")
        self.toplevel.sep()
        self.toplevel.stmt(inspect.getsource(reify))
        self.toplevel.stmt(inspect.getsource(InputWrapper))
        return self.m


def get_codegen(request):
    return CodeGenerator(request)
