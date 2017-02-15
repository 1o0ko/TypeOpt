import collections

DOUBLE_DASH = '--'
DASH = '-'
UNDER_SCORE = '_'


def parsing_rule(func):
    '''
    Decorator that sets the _is_rule attribute in the input callable
    '''
    func._is_rule = True
    return func


def update(key, args, predicate, transform):
    '''
    Conditionally updates keys in a dictionary
    '''
    if predicate(key):
        key, key_old = transform(key), key
        args[key] = args.pop(key_old)

    return key, args


class FilterClass(type):

    '''
    A metaclass that extracts all methods that have
    a _is_rule attribute and lists them in order in
    the _is_rules attribute of the class.
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
        result._is_rules = [
            value for value in namespace.values() if hasattr(
                value, '_is_rule')]
        return result


class BaseParser(metaclass=FilterClass):

    '''
    A callable class that parses dictionaries.
    It may be given methods decorated with @parsing_rule and it will apply
    them on the input string in definition order.
    '''

    def __call__(self, key, args):
        _key = key

        # Loop on filters and apply them on the key
        for rule in self._is_rules:
            _key, args = rule(self, _key, args)

        return args


class DictParser(BaseParser):

    def __init__(self, typed):
        self.typed = typed

    @parsing_rule
    def cast_values(self, k, args):
        type_annotation = next((t for (line, t) in self.typed
                                if k in line), None)

        if type_annotation and isinstance(args[k], str):
            clean_value = args[k].replace("=", "")
            args[k] = eval("%s(%s)" % (type_annotation, clean_value))

        return k, args

    @parsing_rule
    def remove_double_dash(self, k, args):
        return update(k, args,
                      lambda k: DOUBLE_DASH in k,
                      lambda k: k.replace(DOUBLE_DASH, ""))

    @parsing_rule
    def dash_to_underscore(self, k, args):
        return update(k, args,
                      lambda k: DASH in k,
                      lambda k: k.replace(DASH, UNDER_SCORE))

    @parsing_rule
    def lowercase_if_necessary(self, k, args):
        return update(k, args,
                      lambda k: any(map(str.isupper, k)),
                      lambda k: k.lower())


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
