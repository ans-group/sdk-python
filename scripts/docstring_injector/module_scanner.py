""" """
import importlib
import inspect
import pkgutil

exempt_modules = ['tests', 'base', 'config', 'exceptions']
exempt_functions = ['auth_test']


class Function():
    def __init__(self, submodule_name, submodule, class_name, class_imp, function_name, function_imp):
        self.submodule_name = submodule_name
        self.submodule = submodule
        self.class_name = class_name
        self.class_imp = class_imp
        self.function_name = function_name
        self.function_imp = function_imp

    def __eq__(self, function):
        return self.submodule_name == function.submodule_name and \
            self.class_name == function.class_name and \
            self.function_name == function.function_name


def is_valid_submodule(path):
    for exemption in exempt_modules:
        if exemption in path:
            return False
    return True


def load_module_from_spec(spec):
    return importlib._bootstrap._load(spec)


def is_ukfast_base(class_name):
    return 'UKFastAPI.base' in class_name


def is_valid_function(function_name):
    for exemption in exempt_functions:
        if exemption in function_name:
            return False

    if is_ukfast_base(function_name) or function_name.startswith('_'):
        return False

    return True


def get_functions(module):
    functions = []
    for importer, modname, _ in pkgutil.walk_packages(module.__path__):

        # DEBUG
        # if 'Account' in modname or 'Billing' in modname:
        # continue
        # DEBUG

        spec = pkgutil._get_spec(importer, modname)
        if not is_valid_submodule(spec.origin):
            continue

        submodule_name = spec.parent

        submodule = load_module_from_spec(spec)

        if '__init__' in submodule.__file__:
            continue

        print(submodule.__file__)

        # Get classes from module.
        for _, class_imp in inspect.getmembers(submodule, predicate=inspect.isclass):

            class_name = class_imp.__name__

            if isinstance(class_imp, type) and not is_ukfast_base(class_imp.__module__):

                # Get functions from classes.
                for function_name, function_imp in inspect.getmembers(
                        class_imp, predicate=inspect.isfunction):
                    if not is_valid_function(function_name):
                        continue

                    new_function = Function(
                        submodule_name,
                        submodule,
                        class_name,
                        class_imp,
                        function_name,
                        function_imp
                    )

                    flag = True
                    for function in functions:
                        if function == new_function:
                            flag = False

                    if flag:
                        functions.append(
                            new_function
                        )
                        print('{}:{}:{}'.format(submodule_name, class_name, function_name))
    return functions
