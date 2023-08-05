# Brian2Lava


The goal of this open source project is to develop a [Brian2](https://github.com/brian-team/brian2) interface for the neuromorphic computing framework [Lava](https://github.com/lava-nc/lava), called Brian2Lava, to facilitate deployment of brain-inspired algorithms on Lava-supported neuromorphic hardware and emulator backends. Brian2 is an open source Python package developed and used by the computational neuroscience community to simulate spiking neural networks.

The readme contain a quick introduction. For more detailed information visit our website and our documentation.

* [Website](https://brian2lava.gitlab.io/)
* [Documentation](https://brian2lava.gitlab.io/docs)
## Installation

Brian2Lava currently supports Lava with `CPU` backend. We’re working on `Loihi` support. Please feel free to test Brian2Lava and report issues.

The installation of `Brian2Lava` is provided via the the Python Package Index (`pip`):

```
pip install brian2lava
```

Note: perhaps also `conda` will be supported later.

## Getting started

Using Brian2Lava requires only two steps.

First, import the package:

```
import brian2lava
```

Second, set the lava device and your hardware backend (currently only `CPU` is supported, we’re actively working on `Loihi`):

```
set_device('lava', hardware='CPU')
```

For a full example visit the ['Getting Started' page on our website](https://brian2lava.gitlab.io/).

