# video_datasets_api
Video datasets (HMDB-51, EPIC-Kitchens, Something-Something-V1, etc.) tools and API

It consists of extracting videos into frames, and reading annotations and returning training splits, labels and class keys.

# Installation

You can use the tools as is. For the API, it is easier if you install.
`python setup.py develop`

Then, you can import the package.

```python
from video_datasets_api.something_something_v1 import NUM_CLASSES
print(NUM_CLASSES)    # 174
```
