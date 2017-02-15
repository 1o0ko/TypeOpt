"""
Usage: example.py PATH [options]

Arguments:
    PATH    path to example file

Options:
    -l, --limit=<int>           Limit on the number of parsed lines

    --some-flag                 Some boolean flag
    --float-option=<float>      Optionally change value to something other
                                float [default: 0.2]
"""
import itertools

from typeopt import Arguments

if __name__ == '__main__':

    args = Arguments(__doc__, version='GloVe 0.1')

    print(args)
    with open(args.path) as file_:
        for index, line in enumerate(itertools.islice(file_, 10)):
            print("Line {0}: {1}".format(index, line))
