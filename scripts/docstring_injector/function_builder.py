import inspect

exempt_functions = ['delete', 'save']


def generate_docstring_from_swagger_object(swagger_object):
    description = swagger_object.description
    params = swagger_object.params

    kwargs = ''
    for kwarg in params:
        kwargs += '\n            {}{} - {}'.format(
            '*' if kwarg.get('required') else '',
            kwarg.get('name'),
            '{' + kwarg.get('type') + '}',
            kwarg.get('description', ''),
            ('eg: ' + str(kwarg['example'])) if kwarg.get('example') else '',
        )

    if len(kwargs) == 0:
        kwargs = '\tNone'

    return_type = '\tNone'

    if swagger_object.request_type not in exempt_functions:
        return_type = swagger_object.object_type
        if swagger_object.request_type == 'list':
            return_type = '[' + return_type + ']'

    docstring = '        """{}\n\n        ### args:\n            None\n\n        ### kwargs:        {}\n\n        ### returns:\n            {}"""'.format(
        description if description else '', kwargs, return_type)
    return docstring


def generate_function(function, swagger_doc):
    docstring = generate_docstring_from_swagger_object(swagger_doc)
    target_function = '{}{}'.format(
        function.function_imp.__name__,
        str(inspect.signature(function.function_imp))
    )
    declaration = 'def {}'.format(target_function)
    code = 'return super().{}'.format(target_function)
    return '    {}\n{}\n        {}'.format(declaration, docstring, code)
