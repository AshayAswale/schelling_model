# SCHELLING MODEL

### Language: python3.8.5
### Imports Used:

```py
import numpy as np
import matplotlib.pyplot as plt
import random
```

## Code Running Instructions
You can execute the code with a simple python run command:
```bash
python3 schelling_model.py
```

## To Edit the parameters
In the file `schelling_model.py` scroll to the top, and change the global parameters to change the code dependant parameters

Parameters are as follows:
```py
p = 0.8         # Fraction of cells filled
t1 = 3          # Satisfaction threshold
t2 = 5          # Will only be used if t1_ratio is not 1. Second satisfaction Threshold
t1_ratio = 0.8  # When you want 0.8/0.2 ratio of t1 and t2, set this as 0.8
rounds = 1000   # Maximum rounds that should run
```
