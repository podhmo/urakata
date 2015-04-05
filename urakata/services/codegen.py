# -*- coding:utf-8 -*-
import inspect
import json
from collections import OrderedDict
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

    def emit_dict(self, fmt, data):
        stmt = fmt.format(json.dumps(data, indent=2, ensure_ascii=False))
        for line in stmt.split("\n"):
            self.m.stmt(line)

    def build_main(self, data, emitter):
        self.m.stmt("root = args[0]")
        self.emit_dict("defaults = {}", data["defaults"])
        self.emit_dict("usages = {}", data["usages"])
        self.emit_dict("contents = {}", [(d["name"], d["content"]) for d in data["templates"]])
        self.m.stmt("config = {}(None, root, defaults=defaults, usages=usages, contents=contents)".format(
            emitter.config.__class__.__name__
        ))
        self.m.stmt("emitter = {}(None, root, config)".format(emitter.__class__.__name__))
        self.m.stmt("emitter.emit()")

    def codegen(self, extracted, emitter):
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

        # main
        with self.m.def_("main", "args"):
            self.build_main(extracted, emitter)
        with self.m.if_("__name__ == '__main__'"):
            self.m.stmt("logging.basicConfig(level=logging.INFO)")
            self.m.stmt("main(sys.argv[1:])")
        return self.m


def get_codegen(request):
    return CodeGenerator(request)
