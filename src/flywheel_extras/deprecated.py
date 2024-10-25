import warnings


class FnCollectorContainer:
    def __init_subclass__(cls, **kwargs):
        with warnings.catch_warnings():
            warnings.filterwarnings('once')
            warnings.warn('FnCollectorContainer is deprecated, just delete it', DeprecationWarning)
