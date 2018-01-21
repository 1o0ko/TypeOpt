# typeopt
Typed version of [docopt](https://github.com/docopt/docopt) thanks to metaclasses. To be used in Machine Learning experiments. 

```python
"""
Usage: example.py PATH [options]

Arguments:
    PATH    path to example file

Options:
    -l, --limit=<int>           Limit on the number of parsed lines

    --some-flag                 Some boolean flag
    --float-option=<float>      Optionally change value to something other
                                float [default: 0.2]
    --api-key=<str>             API KEY to your SaaS provider
"""
from typeopt import Arguments

if __name__ == '__main__':

    arguments = Arguments(__doc__, version='example 0.2')

    print(arguments)
```

Sample usage can be found in my repository with [short, self-contained tensorflow examples](https://github.com/1o0ko/tf-kata).
