# video_datasets_api
Video datasets (HMDB-51, EPIC-Kitchens, Something-Something-V1, etc.) tools and API

**Key features**  
- Extract videos into frames
  - If mjpeg dataset, just extract jpegs losslessly. Faster and better quality.
- Extract optical flows using multiple GPUs
- Definitions without having to load annotations (`NUM_CLASSES`)
- Read annotations (e.g. labels, class key strings)


# Installation

You can use the tools as is. For the API, it is easier if you install.
`python setup.py develop`

Then, you can import the package.

```python
from video_datasets_api.something_something_v1 import NUM_CLASSES
print(NUM_CLASSES)    # 174
```
