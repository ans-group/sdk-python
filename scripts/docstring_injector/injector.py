""" """
import inspect
import collections
from typing import NamedTuple
import module_scanner
import function_builder
import swagger


def inject_docstrings(module, url):
    functions = module_scanner.get_functions(UKFastAPI)
    swagger_cache = {}

    for function in functions:

        # Currently targets v1 and messes this up.
        if function.submodule_name == 'eCloud':
            continue

        if not swagger_cache.get(function.submodule_name):
            swagger_cache[function.submodule_name] = swagger.SwaggerDoc(
                function.submodule_name, url)

        for swagger_object in swagger_cache[function.submodule_name].swagger_objects:
            object_name = function.class_name.replace('Manager', '')
            object_name_alt = object_name + 's'
            if (swagger_object.object_type == object_name or swagger_object.object_type == object_name_alt) and swagger_object.request_type == function.function_name:
                generated_function = function_builder.generate_function(
                    function,
                    swagger_object
                )

                function.generated_function = generated_function

    modules = {}
    for function in functions:
        filename = function.submodule.__file__

        if not modules.get(filename):
            modules[filename] = {}

        if not modules[filename].get(function.class_name):
            modules[filename][function.class_name] = []
        source_lines = inspect.getsourcelines(function.class_imp)
        function.__dict__['class_end_lineno'] = len(source_lines[0]) + source_lines[1]
        modules[filename][function.class_name].append(function)

        if hasattr(function, 'generated_function'):
            print('!{} - {}'.format(function.class_name, function.function_name))

    # Sort class within module by ending line number.
    for module_name, class_list in modules.items():
        modules[module_name] = collections.OrderedDict(
            sorted(
                class_list.items(),
                key=lambda key_values: key_values[1][0].class_end_lineno))
        print()

    print()
    for module_name, class_list in modules.items():
        filepath = './scripts/docstring_injector/build/' + \
            module_name[module_name.find('UKFastAPI'):]

        buffer = ''
        with open(filepath, 'r+') as file:
            for line_number, line in enumerate(file):
                for class_name, class_ in class_list.items():
                    for function_ in class_:
                        if function_.class_end_lineno == line_number:
                            if hasattr(function_, 'generated_function'):
                                buffer += function_.generated_function + '\n\n'
                buffer += line
        print(buffer)
        print()


if __name__ == "__main__":
    import UKFastAPI
    inject_docstrings(UKFastAPI, 'https://developers.ukfast.io/api/documentation/')
