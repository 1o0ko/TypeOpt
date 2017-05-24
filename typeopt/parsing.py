import collections

DOUBLE_DASH = '--'
DASH = '-'
UNDER_SCORE = '_'
STRING = 'str'

def parsing_rule(func):
    '''
    Decorator that sets the _rule attribute in the input callable
    '''
    func._rule = True
    return func


class FilterClass(type):

    '''
    A metaclass that extracts all methods that have
    a _rule attribute and lists them in order in
    the _rules attribute of the class.
    '''

    def __prepare__(name, bases, **kwds):
        # This returns an OrderedDict to host the namespace of
        # the created  class
        return collections.OrderedDict()

    def __new__(metacls, name, bases, namespace, **kwds):
        # This method returns an instance of the metaclass
        # aka the created class.

        # Just call the standard creation method
        result = type.__new__(metacls, name, bases, dict(namespace))

        # Process all namespace items and extract the marked ones
        result._rules = [
            value for value in namespace.values() if hasattr(value, '_rule')]
        return result


class BaseParser(metaclass=FilterClass):

    '''
    A callable class that parses dictionaries.
    It may be given methods decorated with @parsing_rule and it will apply
    them on the input string in definition order.
    '''

    def __call__(self, key, value):
        _key, _value = key, value
        for rule in self._rules:
            _key, _value = rule(self, _key, _value)

        return _key, _value


class DictParser(BaseParser):
    '''
    Processes the dictionary and applies set of rules on it's keys
    '''

    def __init__(self, typed):
        self.typed = typed

    @parsing_rule
    def cast_values(self, k, value):
        type_annotation = next((t for (line, t) in self.typed
                                if k in line), None)

        if type_annotation and isinstance(value, str):
            clean_value = value.replace("=", "")
            if type_annotation != STRING:
                value = eval("%s(%s)" % (type_annotation, clean_value))
            else:
                value = clean_value

        return k, value

    @parsing_rule
    def remove_double_dash(self, k, v):
        if DOUBLE_DASH in k:
            k = k.replace(DOUBLE_DASH, "")
        return k, v

    @parsing_rule
    def dash_to_underscore(self, k, v):
        if DASH in k:
            k = k.replace(DASH, UNDER_SCORE)
        return k, v

    @parsing_rule
    def lowercase_if_necessary(self, k, v):
        if any(map(str.isupper, k)):
            k = k.lower()

        return k, v


def main():
    ''' main function '''
    import copy

    msp = DictParser([])

    args = {'--max-length': 100}
    parsed_args = msp('--max-length', copy.deepcopy(args))

    print(args)
    print(parsed_args)


if __name__ == '__main__':
    main()
