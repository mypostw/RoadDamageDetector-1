import sys
import json
import random

from os.path import basename

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams

rcParams['figure.figsize'] = 16, 20
rcParams['figure.dpi'] = 240
rcParams['font.size'] = 18

linestyles = ['-', '--', ':', '-.']



def extract(logs, keys):
    def _extract(log):
        items = []
        for key in keys:
            try:
                item = log[key]
            except:
                item = None
            items.append(item)
        return items
    L = list(zip(*[_extract(log) for log in logs]))
    return np.array(L, dtype=np.double)


if len(sys.argv) < 2:
    print("Usage $python3 showreport.py <path to log file>")
    exit(0)


logfile_path = sys.argv[1]
with open(logfile_path, "r") as f:
    logs = json.load(f)

L = extract(logs, keys=[
    "iteration",
    "main/loss",
    "main/loss/conf",
    "main/loss/loc"
])

labels = ["confidence loss", "location loss", "overall loss"]

iteration, loss = L[0], L[1:]

ax1 = plt.subplot(211)

for loss_, label in zip(loss, labels):
    plt.plot(iteration, loss_, label=label)
plt.legend(prop={'size': 16})

keys = [
    'validation/main/ap/D00',
    'validation/main/ap/D01',
    'validation/main/ap/D10',
    'validation/main/ap/D11',
    'validation/main/ap/D20',
    'validation/main/ap/D40',
    'validation/main/ap/D43',
    'validation/main/ap/D44',
    'validation/main/map'
]

L = extract(logs, keys=["iteration"] + keys)

labels = [basename(key) for key in keys]

iteration, aps = L[0], L[1:]

plt.subplot(212, sharex=ax1)
plt.ylim([0, 1])
for ap, label in zip(aps, labels):
    masks = np.logical_not(np.isnan(ap))
    plt.plot(iteration[masks], ap[masks], linestyle=random.choice(linestyles), label=label)

plt.xlabel("iteration")
plt.legend(loc='center left', bbox_to_anchor=(1, 0.815), numpoints=1)

plt.show()
