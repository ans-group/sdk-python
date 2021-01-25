""" The Base API object for all modules """
import os
import json
import logging
from collections import namedtuple
import enum

import requests

from UKFastAPI import config
from UKFastAPI import exceptions

# pylint:disable=too-few-public-methods, protected-access

logging.basicConfig(level=logging.DEBUG)


class Actions(enum.Enum):
    """ Enum used to define request types within the IManagedObject Action method. """
    POST = 0
    PUT = 1


class IApiObj():
    """ The interface that handles retrieving object attributes that might not exist. """

    def __getattr__(self, name):
        return None


class ISetAttr(IApiObj):
    """ Interface for handling attribute writes. """

    def __setattr__(self, name, value):
        if self._identifier and name == self._identifier and not self._override_setattr_blocking:
            raise exceptions.UKFastSDKException(
                'Cannot set {} attribute on {} objects.'.format(name, type(self)))
        vars(self)[name] = value


class IUrlCreator(IApiObj):
    """ Creates a url. """

    def _get_url(self):
        # pylint:disable=protected-access
        return '{}/{}'.format(self._manager._url, vars(self)[self._identifier])

    def _create_url(self, data):
        # pylint:disable=protected-access
        url = self._url
        if not url:
            url = self._manager._url
        return '{}/{}'.format(url, data)


class IObjectCreator(IApiObj):
    """ An abstraction used to create objects. """

    def _create_object(self, data):
        if len(data) > 1:
            return [self._type(self, entry) for entry in data]
        return self._type(self, data[0])


class IGettable(IObjectCreator, IUrlCreator):
    """ The interface that handles getting objects via the API. """

    def _get(self, url, **kwargs):
        data = self._base._get(url if url else self._url, **kwargs)
        if data:
            return super()._create_object(data)
        return None

    def get(self, identifier, **kwargs):
        """ Get an object matching the given identifier. """
        return self._get(super()._create_url(identifier), **kwargs)


class ICreateable(IGettable, IObjectCreator, IUrlCreator):
    """ The interface that handles creating objects via the API. """

    def _create(self, url, **kwargs):
        data = self._base._post(url, **kwargs)
        return None if not data else super()._create_object(data)

    def create(self, **kwargs):
        # pylint:disable=protected-access
        """ Create an object. """
        obj = self._create(self._url, **kwargs)
        return super()._get(super()._create_url(vars(obj)[obj._identifier]))


class IUpdateable(IUrlCreator, ISetAttr):
    """ The interface that handles updating objects via the API. """

    def _update(self, url, **kwargs):
        self._base._patch(url, **kwargs)

    def save(self):
        # pylint:disable=protected-access
        """ Save object changes. """
        self._update(
            self._url,
            **{
                k: v for k, v in vars(self).items() if not k.startswith('_')
            }
        )


class IDeleteable(IUrlCreator):
    """ The interface that handles deleting objects via the API. """

    def _delete(self, url, **kwargs):
        self._base._delete(url, **kwargs)

    def delete(self, **kwargs):
        """ Used to delete the object. """
        # pylint:disable=protected-access
        identifier_ = vars(self).get(self._identifier)
        if not identifier_:
            raise exceptions.UKFastSDKException(
                'Object has not been assigned an _identifier \
                but implements the IDeleteable interface.')
        self._delete(self._url, **kwargs)


class IListable(IApiObj):
    """ Ensures a list is properly formatted. """

    def list(self, **kwargs):
        """ The interface for retrieving a list of objects. """
        result = self._get(self._url, **kwargs)
        if not result:
            return []
        if isinstance(result, list):
            return result
        return [result]


class IBareObject(IApiObj):
    """ Used if an object only has a get operation. """

    def __init__(self, base, url):
        self._base = base
        self._url = url

        # Sometimes objects received from the API are empty and represented by a 404.
        # Since bare objects are instantiated as the result of a
        # base manager being created (eg: Billing creating the DirectDebitManager),
        # this allows bare objects to fail silently on 404s.
        data = None
        try:
            data = self._base._get(self._url)
        except exceptions.UKFastAPIException:
            logging.debug(self.__name__)

        if data:
            vars(self).update(data[0])


class IIdentifierOnlyManager(IApiObj):
    """
    Used when we only want an object to contain an identifier.
    This stops object creation recursion where object A contains
    a list of object B's, and object B contains a list of object A's.
    This design is present in certain UKFast modules.
    """

    def __init__(self, base, url):
        self.base = base
        self.url = url

    def list(self):
        """ Provides a list of object identifiers. """
        data = self.base._get(self.url)
        objects = []
        if data:
            for entry in data:
                objects.append((namedtuple('identifier', 'id'))(entry.get('id')))
        return objects


class IManager(IGettable, IListable):
    """ Used by API object managers. """

    def __init__(self, base, type_, url):
        self._base = base
        self._type = type_
        self._url = url


class IManagedObject(IUrlCreator):
    """ Deals with the basic init of the API objects """

    _identifier = 'id'

    def __init__(self, manager, data):
        if not data:
            # This needs to stay due to objects like
            # eCloud>Vms>Tags creation not returning any data.
            return
        vars(self).update(data.items())
        self._manager = manager
        self._base = manager._base
        self._url = super()._get_url()

    def _action(self, action, url, **kwargs):
        """ Used to create a simple bridge from a user facing function to a requests call. """
        if action == Actions.POST:
            return self._base._post(self._url + url, **kwargs)
        if action == Actions.PUT:
            return self._base._put(self._url + url, **kwargs)
        return None


class BaseApi():
    """ The Base API class used to abstract requests. """
    _page_str = 'page'
    _per_page_str = 'per_page'
    _all_str = 'all'
    _pagination_str = 'pagination'

    def __init__(self, auth):
        if not auth:
            auth = os.getenv(config.UKF_API_KEY)
        self.auth = auth

    def auth_test(self):
        """ Ensure we can properly authenticate. """
        try:
            logging.warning('%s with %s',
                            config.BASE_URL + vars(self).get('_url'),
                            self.auth)

            response = requests.get(
                config.BASE_URL + vars(self).get('_url'),
                headers={'Authorization': self.auth}
            )

            if response.status_code == 401:
                raise exceptions.UKFastAPIException(
                    'Provided authentication token retured access denied.')
            if response.status_code != 404:
                response.raise_for_status()
        except Exception as exception:
            logging.exception('Failed authentication check.')
            raise exception
        return True

    def _request(self, method, url, **kwargs):
        # Make request.
        response = None
        try:
            logging.info(
                '%s - %s',
                config.BASE_URL + url,
                kwargs
            )

            json_ = {k: v for k, v in kwargs.items() if not isinstance(v, IApiObj)}
            response = method(
                config.BASE_URL + url,
                headers={'Authorization': self.auth},
                json=json_
            )

            response.raise_for_status()
        except requests.HTTPError as _:
            if response is not None and response.text:

                response_json = json.loads(response.text)
                if response_json:
                    errors = response_json.get('errors')
                    if errors:
                        for error in errors:
                            raise exceptions.UKFastAPIException(
                                '{} - {}'.format(
                                    error.get('title'),
                                    error.get('detail')
                                )
                            )
            return None

        # Parse response.
        if not response or not response.text or not json.loads(response.text):
            return None

        response_json = json.loads(response.text)

        # Check for errors in response.
        # errors = response_json.get('errors')
        # if errors:
        # Coverage: Getting flagged as we're not testing a 200 with an error in the body.
        # logging.error([error.title for error in errors])

        # Return response object.
        return (namedtuple('response', 'status data meta'))(
            response.status_code,
            response_json.get('data'),
            response_json.get('meta')
        )

    def _get(self, url, **kwargs):
        """ Used to make get (read) requests to the given url. """
        results = []
        kwargs_alt = dict(kwargs)

        page = kwargs.get(self._page_str, 1)
        if kwargs_alt.get(self._page_str):
            del kwargs_alt[self._page_str]

        per_page = kwargs.get(self._per_page_str, config.DEFAULT_PER_PAGE)
        if kwargs_alt.get(self._per_page_str):
            del kwargs_alt[self._per_page_str]

        all_ = kwargs.get(self._all_str, False)
        if kwargs_alt.get(self._all_str):
            del kwargs_alt[self._all_str]
            per_page = config.MAX_PER_PAGE

        while True:
            response = self._request(
                requests.get,
                '{}?{}={}&{}={}'.format(
                    url,
                    self._per_page_str,
                    per_page,
                    self._page_str,
                    page
                )
            )

            try:
                if not response:
                    return None

                if isinstance(response.data, list):
                    for result in response.data:
                        results.append(result)
                else:
                    results.append(response.data)

                # Stop if we aren't requesting all results.
                if not all_:
                    break

                # Stop if there are no more pages to request.
                current_page = response.meta[self._pagination_str]['current_page']
                total_pages = response.meta[self._pagination_str]['total_pages']
                if current_page >= total_pages:
                    break

                page += 1
            except Exception as _:  # pragma: no cover
                raise exceptions.UKFastAPIException(  # pragma: no cover
                    'An unexpected response was received from the UKFast API.')  # pragma: no cover

        return results

    def _post(self, url, **kwargs):
        """ Used to make post (create) requests to the given url. """
        return [self._request(requests.post, url, **kwargs).data]

    def _patch(self, url, **kwargs):
        """ Used to make patch (updated) requests to the given url. """
        return self._request(requests.patch, url, **kwargs)

    def _delete(self, url, **kwargs):
        """ Used to make delete requests to the given url. """
        return self._request(requests.delete, url, **kwargs)

    def _put(self, url, **kwargs):
        """ Used to make put requests to the given url. """
        return self._request(requests.put, url, **kwargs)
