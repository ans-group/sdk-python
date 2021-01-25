""" VCR related utils functions. """
import logging
import vcr

logging.basicConfig()
vcr_log = logging.getLogger("vcr")
vcr_log.setLevel(logging.INFO)


def decorate_funcs(decorator):
    """ Decorates all functions within a class. """
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


def generate_vcr_decorator(cassette_dir):
    """ Generates a standard VCR object. """

    return vcr.VCR(
        cassette_library_dir=cassette_dir,
        filter_headers=['Authorization'],
        path_transformer=vcr.VCR.ensure_suffix('.yml'),
        # record_mode='all'  # Used to do the local testing to create the cassettes.
        record_mode='none'  # Used by CI utilising the pre-recorded cassettes.
    ).use_cassette
