============
Installation
============

For Anaconda distribution (for now only Linux64 and Win64 supported) you can install from personal channel::

    conda install -c ondrolexa pywerami

For other platforms install dependencies using conda::

    conda install numpy matplotlib scipy pyqt

or by any other mechanism (see `Installing Scientific Packages <https://packaging.python.org/science/>`_).

Than install pywerami directly from github using pip::

    https://github.com/ondrolexa/pywerami/archive/master.zip

For upgrade use::

    pip install --upgrade --upgrade-strategy only-if-needed \
      https://github.com/ondrolexa/pywerami/archive/master.zip
          

To install most recent (and likely less stable) development version use::

    https://github.com/ondrolexa/pywerami/archive/develop.zip


For upgrade to latest development version use::

    pip install --upgrade --upgrade-strategy only-if-needed \
      https://github.com/ondrolexa/pywerami/archive/develop.zip