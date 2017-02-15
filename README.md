# typeopt
Typed version of docopt. Used in Machine Learning experiments. 


```python
"""
Usage: example.py PATH [options]

Arguments:
    PATH    path to example file

Options:
    -l, --limit=<int>           Limit on the number of parsed lines

    --some-flag                 Some boolean flag
    --float-option=<float>      Optionally change value to some other
                                float [default: 0.2]
"""
from typeopt import Arguments

if __name__ == '__main__':

    arguments = Arguments(__doc__, version='example 0.1')

    print(arguments)
```
