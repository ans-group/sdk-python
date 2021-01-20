import sys
import requests
import yaml
from setuptools import find_packages

request_mappings = {
    'list': 'list',
    'get': 'get',
    'post': 'create',
    'patch': 'save',
    'delete': 'delete'
}


class SwaggerDoc():
    def __init__(self, name, url):
        self.name = name
        response = requests.get(url + name.lower())
        response.raise_for_status()
        self.swagger_objects = self.get_swagger_info(
            yaml.load(response.text))

    def harvest_param(self, param):
        return {
            'name': param['name'],
            'type': param['schema']['type'],
            'required': param['required'],
            'description': param.get('description'),
            'example': param.get('example'),
        }

    def get_swagger_params(self, request_type, request_params, components, special_params=[]):
        ret_params = []

        # Method 1
        # get requests from managers require the object id.
        params = request_params.get('parameters')
        if params and (request_type == 'get' or request_type == 'list'):
            for param in params:

                # Because of the way we've layed out the API objects in the SDK,
                # we don't want the params to include an identifier that is
                # half way down the request, as that will already exist in the parent object.
                # For example:
                #     /safedns/v1/zones/{zone_name}/records
                #                        ^^^^^^^^^
                # We don't want the zone_name param to be added to our list of params,
                # because the use will not need to provide that, it will already exist
                # within the Zone object that they are calling the record object from.
                if param['name'] in request_params.get(
                        'summary', '') and not request_params['summary'].endswith(
                        '{' + param['name'] + '}'):
                    continue

                ret_params.append(self.harvest_param(param))
            return ret_params

        # Method 2
        # All other request types have their params found in the request body.
        schema = request_params.get('requestBody', {}).get(
            'content', {}).get('application/json', {}).get('schema', {})
        params = schema.get('properties', {})
        required = True if request_params.get('requestBody', {}).get('required') else []
        # If we have params at this point, then the requestBody had the params written directly into it.
        # If not, the requestBody would have used a ref to the components section later in the swagger doc.

        # Method 3
        # Check if this is a component ref.
        if not params:
            component_ref = schema.get('$ref', {})
            if component_ref:
                component_ref = component_ref.split('/')[-1]
                params = components.get('schemas', {}).get(component_ref, {}).get('properties', {})
                required = components.get('schemas', {}).get(component_ref, {}).get('required', {})

        if special_params:
            for param in special_params:
                ret_params.append(self.harvest_param(param))

        # Compile params
        if params:
            for param_name, param_details in params.items():
                if not param_details.get('readOnly'):
                    ret_params.append(
                        {'name': param_name, 'type': param_details.get('type'),
                         'description': param_details.get('description'),
                         'example': param_details.get('example', None),
                         'required': True
                         if isinstance(required, bool) and required is True else param_name in
                         required})
            return ret_params

        return None

    def get_swagger_info(self, yaml_):
        swagger_objects = []

        special_parameters_object = None
        for path, more in yaml_['paths'].items():
            for request_type, request_params in more.items():

                # Determine whether this is what we call a 'list' operation.
                if request_type == 'get':
                    for param in request_params.get('parameters', {}):
                        if param.get('name', {}) == 'page':
                            request_type = 'list'

                if request_type == 'parameters':
                    special_parameters_object = request_params
                    continue

                object_name = request_params.get('tags')
                if not object_name:
                    print('Failed to get object name.')
                object_name = object_name[0]

                swagger_object = SwaggerObject(
                    object_name, request_type, request_params.get('description'))

                swagger_components = yaml_.get('components', {})
                params = self.get_swagger_params(
                    request_type,
                    request_params,
                    swagger_components,
                    special_parameters_object
                )

                if params:
                    for param in params:
                        swagger_object.add_param(param)
                swagger_objects.append(swagger_object)

        return swagger_objects


class SwaggerObject():
    def __init__(self, object_type, request_type, description):
        self.object_type = object_type
        self.request_type = request_mappings.get(request_type, request_type)
        self.description = description
        self.params = []
        if request_type == 'list':
            self.params.append({
                'name': 'all',
                'type': 'boolean',
                'description': 'Retrieve all objects available',
            })

    def add_param(self, param):
        self.params.append(param)

    def __repr__(self):
        return '{}: {} ({})\n\t{}'.format(
            self.object_type,
            self.request_type,
            self.description,
            '\n\t'.join([
                '{}{} ({}){}{}'.format(
                    '*' if param.get('required') else '',
                    param['name'],
                    param['type'],
                    ' - {}'.format(param['description']) if param['description'] else '',
                    ' [eg: {}]'.format(param['example']) if param.get('example') else '',
                ) for param in self.params
            ])
        )
