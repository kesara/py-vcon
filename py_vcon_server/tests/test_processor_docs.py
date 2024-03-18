#!/usr/bin/python3

""" Generate doc/README.md for processor plugins """
import typing
import inspect
import py_vcon_server.processor


CLASS_TEMPLATE = """
## {class_name}  version: {class_version}

{class_path}
 - {class_title}

{class_description}

#### Fields:
"""

def sort_types(type_set: typing.Set[typing.Type], head: typing.Type) -> typing.List[typing.Type]:
  sorted_list = sorted(type_set.copy(), key = lambda cls: cls.__name__)
  sorted_list.remove(head)
  sorted_list.insert(0, head)

  return(sorted_list)


def build_processors_doc() -> str:
  readme_text = ""
  processors = set()
  processors.add(py_vcon_server.processor.VconProcessor)
  init_options = set()
  init_options.add(py_vcon_server.processor.VconProcessorInitOptions)
  options = set()
  options.add(py_vcon_server.processor.VconProcessorOptions)

  processor_class_data: typing.Dict[typing.Type, typing.Dict[str, str]] = {}
  processor_type = py_vcon_server.processor.VconProcessor
  processor_name = "VconProcessor"
  class_data: typing.Dict[str, str] = {}
  class_data["class_name"] = processor_name
  class_data["class_path"] = processor_type.__module__ + "." + processor_type.__name__
  class_data["class_title"] = "Abstract VconProcessor class"
  class_data["class_version"] = ""
  class_data["class_description"] = "{}".format(processor_type.__doc__)
  processor_class_data[processor_type] = class_data

  processor_names = py_vcon_server.processor.VconProcessorRegistry.get_processor_names()
  for processor_name in processor_names:
    processor_inst = py_vcon_server.processor.VconProcessorRegistry.get_processor_instance(
      processor_name)
    processor_type = type(processor_inst)
    processors.add(processor_type)
    class_data = {}
    class_data["class_name"] = processor_name
    class_data["class_path"] = processor_type.__module__ + "." + processor_type.__name__
    class_data["class_title"] = processor_inst.title()
    class_data["class_version"] = processor_inst.version()
    class_data["class_description"] = processor_inst.description()
    print("adding class defs for: {}".format(processor_name))
    processor_class_data[processor_type] = class_data
    options.add(processor_inst.processor_options_class())
    #init_sig = inspect.signature(processor_inst.__init__)
    #print("{} init: {}".format(processor_name, init_sig))
    #init_options_arg_name = list(init_sig.parameters)[0]
    #init_options_type = init_sig.parameters[init_options_arg_name].annotation
    # TODO: get init_options type from introspection of the plugin __init__ method
    init_options.add(type(processor_inst.init_options))
    print("{} init: {}".format(processor_name, type(processor_inst.init_options)))

  sorted_processors = sort_types(processors, py_vcon_server.processor.VconProcessor)
  sorted_options = sort_types(options, py_vcon_server.processor.VconProcessorOptions)
  sorted_init_options = sort_types(init_options, py_vcon_server.processor.VconProcessorInitOptions)
  #readme_text = "{}".format(sorted_processors)

  for processor in sorted_processors:
    class_data = processor_class_data[processor]
    proc_class_doc = CLASS_TEMPLATE.format(**class_data)
    readme_text += proc_class_doc + "\n\n"

  for init in sorted_init_options:
    init_text = "Init type: {}".format(init.__name__)
    readme_text += init_text + "\n"

  for opt in sorted_options:
    opt_text = "proc opt type: {}".format(opt.__name__)
    readme_text += opt_text + "\n"

  return(readme_text)

def main():
  processor_readme_text = build_processors_doc()

  with open("py_vcon_server/processor/README.md", "w") as readme_file:
    readme_file.write(processor_readme_text)


def test_processor_readme_doc():
  main()

if(__name__ == '__main__'):
  main()

