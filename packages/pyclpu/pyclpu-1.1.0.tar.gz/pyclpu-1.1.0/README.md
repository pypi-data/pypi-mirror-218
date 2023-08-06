**This file describes the module of CLPU utilities and related aspects to users and maintainers.**

# CLPU Utilities

**Abstract:** This module bundels functions which are frequently used for applications at the Centro de Laseres Pulsados, Villamayor, Spain. Although we intend to deliver reliable software solutions, we can not guarantee that every implementation is flawless. We encourage the user to re-read the code and alert us if bugs are found.

:paperclip: The documentation is available in both [`html`](./html/pyclpu/index.html) and [`markdown`](./md/pyclpu/index.md) format.

## Installation

Run `pip install pyclpu` when connected to the internet; or if not connected to the internet `pip install .` within the main folder of the project (where you find also files like `README.md`, `setup.py`, `LICENCE`).

## Use-cases

The following use cases have occured and led to debugged implementations.

### Rename Autosaved Images and Apply Warp Transform

The following code sniffes in a directory `bin` for new files by means of `manager.CatchAndRename` and performs a Warp Transform by means of `image.PerspectiveTransform`. Results are stored in `bin/output_warp` if such directory exists (else in the current working directory).

```
import os
import numpy as np

from pyclpu import image
from pyclpu import manager

chase = manager.CatchAndRename()

chase.directory = "C:\\bin"
chase.prefix = "shot_"
chase.number = 1

warp_it = image.PerspectiveTransform()
warp = []

chase.loop = True
chase.leap = True

while True:
    if chase.flag_new:
        chase.flag_new = False
        warp_it.source = image.imread(os.path.join(chase.directory,chase.filename))
    if warp_it.flag_new:
        warp_it.flag_new = False
        image.imwrite(
            os.path.join(
                chase.directory,
                'output_warp',
                chase.filename
            ),
            warp_it.warped
        )
        np.savetxt(
            os.path.join(
                chase.directory,
                'output_warp',
                manager.strip_extension(chase.filename)+".dat"
            ),
            warp_it.sourcecorners.point_list
        )
```

### Rename Many Files ...

#### ... changing only the extension

```
# EXTERNAL
import os
import sys
import math

from inspect import getsourcefile
from importlib import reload

# INTERNAL
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) # get environment
sys.path.append(os.path.abspath(root)+os.path.sep+"pyclpu")      # add libraries

import manager
reload(manager)

# RENAME .HTML to .MD
chase = manager.CatchAndRename()

chase.directory = root + os.path.sep + "html" +os.path.sep+ "pyclpu"
print(chase.directory)
chase.prefix = ""
chase.extension = "md"
chase.number = math.nan

chase.loop = True

chase.ignored = []

chase.loop = False
```

### Time-of-Flight Analysis

Data of Time-of-Flight detectors comprises a timeline and an amplitude for every recorded temporal bin. The `ToF` class is ment to make data analysis easier. After input of the data and the geometrical situation (location of the detector with respect to the source), it is possible to obtain a spectrum. The x-axis of the output is normalized to be in units of `gamma -1`, where `gamma` is the Lorenz factor. This way the result of the analysis is kept universal without further interpretation regarding the type of particles. If the type of projectiles is known: To obtain the kinetic energy of projectiles it is sufficient to multiply the values with the rest mass energy of the projectiles, e.g. in units of MeV.

```
from pyclpu import metrology

tof_detector = metrology.ToF()
tof_detector.distance = 100
tof_detector.channel = 1
tof_detector.polarity = -1

tof_detector.waveform = "path/to/data.csv"

tof_detector.analyse()
tof_detector.show()
```

The following code sniffes in a directory `bin` for new files by means of `manager.CatchAndRename` and performs a Warp Transform by means of `image.PerspectiveTransform`. Results are stored in `bin/output_warp` if such directory exists (else in the current working directory).

```
import os
import numpy as np
import time

from pyclpu import manager
from pyclpu import metrology

chase = manager.Catch()
chase.directory = "C:\\bin"

tof_detector = metrology.ToF()
tof_detector.distance = 100
tof_detector.channel = 1
tof_detector.polarity = -1

chase.loop = True

while True:
    if len(chase.new) > 0:
        new_file = chase.next()
        tof_detector.waveform = os.path.join(chase.directory,new_file)
        print("WORK "+tof_detector.waveform)
        tof_detector.analyse()
        if tof_detector.status:
            np.savetxt(
                os.path.join(
                    chase.directory,
                    'output_spectrum',
                    manager.strip_extension(new_file)+".spec.dat"
                ),
                np.array([tof_detector.Gminus1,tof_detector.dN_dGminus1]).T,
                header='gamma-1 dN/d(gamma-1)'
            )
```

## Scripts in Modules

### Management Module

#### Rename Incoming Files `CatchAndRename`

This class waits for new files in a directory and renames them to `str(prefix+"_"+number+"."+extension)` according to 
- an optional input variable `prefix` with default `""`, 
- counting up from an optional input variable `number` that defaults to `number = 0`, 
- and without changing the original extension.

The chase for new files is activated by setting the input parameter `loop = True`. The class can be used in a functional way

```
from pyclpu import manager

chase = manager.CatchAndRename(directory = "path/to/directory/", prefix = "any_string", number = 42, loop=True)
```

with 

A more object oriented use case is described below. The chase for new files is activated by setting the input parameter `loop = True` and paused by setting `loop = False`.

```
from pyclpu import manager
import time

chase = manager.CatchAndRename()

chase.directory = "path/to/test"
chase.prefix = "any_string"
chase.number = 42

chase.loop = True

time.sleep(100)

chase.loop = False`

time.sleep(100)

chase.loop = True

```

Files that arrive in the directory during a pause will be ignored when switching on the loop again with `loop = True`.

### Image Module

### Interactive Point Picker `PerspectiveTransform`

The class allows interactive picking of a veriable number of points in a picture. The class can be used in a functional way
```
from pyclpu import image
pick = image.PointPicker(image = image.imread("path/to/test.jpg")) 
```

A more object oriented use case demonstrates how a run can be started after initialization
```
from pyclpu import image
pick = image.PointPicker()
img = image.imread("path/to/test.jpg")
pick.image = img
pick.n = 3
pick.run()
pick.status
True
```

The output is
- the picked points in `pick.point_list` of shape `(n,2)`,
- the status of the execution in `pick.status`, which is True only after a successful run.
    
Note that the source image is not part of the object after processing.
    

#### Warp Transform `PerspectiveTransform`

The class allows to transform a linearly distorted input image into a trapez-corrected view on it. The class can be used in a functional way

```
from pyclpu import image

warp = image.PerspectiveTransform(source = image.imread("path/to/test.jpg")) 
```

with output
- the warped image in `warp.warped` and 
- the coordinates of cornes from the source image stored in `warp.sourcecorners`.

Note that the source image is not part of the object in its final form. The coordinates of the corner points of the target rectangle can also be parsed to the function as `np.array()` of shape `(4,2)` with the keyword `sourcecorners`. A more object oriented use case can deal with loops where all warps have the same source corner coordinates

```
from pyclpu import image

warp_it = image.PerspectiveTransform()

image_stack = image.imread("path/to/directory/with/many/images/")

warp = []

for image in image_stack:
    warp_it.source = image
    warp.append[{"warped" : warp_it.warped, "sourcecorners" : warp_it.sourcecorners}]
```

with results beeing stored in a list `warp`. The dynamic modification of `warp.sourcecorners` is possible.

## Developper's Guide

To get started, clone the project into your working directory `git clone https://srvgitlab.clpu.int/mehret/pyclpu.git` and hop inside `cd pyclpu`. Create the anaconda environment in Anaconda based on the `clpu.yml` file delivered in the main folder of the project, e.g. in the Anaconda prompt with `conda env create -f clpu.yml` and activate it with `conda activate clpu`.

### Integration and Testing

Install actualized versions from the main folder with `pip install .`.

### Export

Before exporting a new version of the module

- increase the version counters in `pyclpu\__init__.py`,
- update the `.yml`file if needed via `conda env export --from-history > clpu.yml`,
- update the documentation via `pdoc --html pyclpu --force && pdoc --template-dir="." -o md pyclpu --force && python text.mako.py`.

Export with `python setup.py sdist` to `dist/`. Then to upload all distributions created under `dist/` execute `twine upload dist/*`or to upload the source distribution with a gpg signature `twine upload dist/pyexample-0.1.0.tar.gz pyexample-0.1.0.tar.gz.asc`. Now the distribution is updated in pyPIP. For the Anaconda version, now,

- update the Anaconda recipe via `grayskull pypi --strict-conda-forge pyCLPU`,
- ...

Close the procedure orderly:
- git-commit the code into the developper's branch `dev` with a note on the new version number,
- git-merge the developper's branch into the main branch `master`.

