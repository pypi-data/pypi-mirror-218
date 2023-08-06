# tcompress

Calculate word counts in a text file!

## Installation

```bash
$ pip install tcompress
```

## Usage

`pycounts` can be used to count words in a text file and plot
results as follows:

```python
from pycounts.pycounts import count_words
from pycounts.plotting import plot_words
import matplotlib.pyplot as plt

file_path = "test.txt"  # path to your file
counts = count_words(file_path)
fig = plot_words(counts, n=10)
plt.show()
```

## License

`tcompress` was created by Talal El Zeini. It is licensed under the terms
of the MIT license.
