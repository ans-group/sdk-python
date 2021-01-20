""" The UKFastAPI Exception implementations. """


class UKFastSDKException(Exception):
    """ An exception for when the SDK has been used incorrectly. """

    def message(self):
        """ The bad SDK message that is raised. """
        return vars(self).get('message', None) or getattr(self, 'args')[0]  # pragma: no cover


class UKFastAPIException(Exception):
    """ An exception for when the API is responding incorrectly. """

    def message(self):
        """ The bad API message that is raised. """
        return vars(self).get('message', None) or getattr(self, 'args')[0]  # pragma: no cover
