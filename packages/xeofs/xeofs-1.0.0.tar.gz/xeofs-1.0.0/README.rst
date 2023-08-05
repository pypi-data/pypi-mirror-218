.. image:: docs/logos/xeofs_logo.png
  :align: center
  :width: 800
  :alt: xeofs logo


|badge_build_status| |badge_docs_status| |badge_version_pypi| |badge_conda_version| |badge_downloads| |badge_coverage| |badge_license| |badge_zenodo|

.. |badge_version_pypi| image:: https://img.shields.io/pypi/v/xeofs
   :alt: PyPI
.. |badge_build_status| image:: https://img.shields.io/github/workflow/status/nicrie/xeofs/CI
   :alt: GitHub Workflow Status (event)
.. |badge_docs_status| image:: https://readthedocs.org/projects/xeofs/badge/?version=latest
   :target: https://xeofs.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |badge_downloads_pypi| image:: https://img.shields.io/pypi/dm/xeofs
    :alt: PyPI - Downloads
.. |badge_coverage| image:: https://codecov.io/gh/nicrie/xeofs/branch/main/graph/badge.svg?token=8040ZDH6U7
    :target: https://codecov.io/gh/nicrie/xeofs
.. |badge_zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.6323012.svg
   :target: https://doi.org/10.5281/zenodo.6323012
   :alt: DOI - Zenodo
.. |badge_license| image:: https://img.shields.io/pypi/l/xeofs
  :alt: License
.. |badge_conda_version| image:: https://img.shields.io/conda/vn/conda-forge/xeofs
   :alt: Conda (channel only)
.. |badge_downloads_conda| image:: https://img.shields.io/conda/dn/conda-forge/xeofs
   :alt: Conda downloads
.. |badge_downloads| image:: https://static.pepy.tech/personalized-badge/xeofs?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads
   :target: https://pepy.tech/project/xeofs
   :alt: Total downloads




Overview
---------------------

``xeofs`` is a Python package that provides a platform for performing Empirical Orthogonal Function (EOF) analysis, a popular technique also known as Principal Component Analysis (PCA). It was born out of a necessity to process and analyse multi-dimensional Earth observation data, where the complexity extends beyond simple 2D matrices to include spatial (longitude, latitude, height), temporal (time, steps, lead times), and other dimensions.

The benefits of using ``xeofs`` include:

- **Multi-dimensional Analysis**: Execute labeled EOF analysis with the extensive features of ``xarray``.
- **Scalability**: Handle large datasets effectively with ``dask``.
- **Speed**: Enjoy quick EOF analysis using ``scipy``'s randomized SVD.
- **Model Validation**: Validate models through bootstrapping.
- **Modular Code Structure**: Incorporate new EOF variants with ease due to the package's modular structure.

Installation
------------

To install the package, use either of the following commands:

.. code-block:: bash

   pip install xeofs

or 

.. code-block:: bash

   conda install -c conda-forge xeofs


Quickstart
----------

In order to get started with ``xeofs``, follow these simple steps:

1. **Import the package**

   .. code-block:: python

      import xeofs as xe

2. **Instantiate the model**

   Select the type of analysis you want to perform (in this case, EOF analysis) and set the parameters. For example, if you want to analyze the first 10 modes, you would use the following code:

   .. code-block:: python

      model = xe.models.EOF(n_modes=10)

3. **Fit the model to your data**

   Fit the model to your data by specifying the dimensions along which the analysis should be performed. Replace 'your_data' and 'your_dimension' with your specific data and dimension:

   .. code-block:: python

      model.fit(your_data, dim=your_dimension)

Congratulations! You have performed your first analysis with ``xeofs``. To further explore the capabilities of ``xeofs``, check the documentation_ and examples_.



Documentation
-------------

For a more comprehensive overview and usage examples, visit the documentation_.

Contributing
------------

Contributions are highly welcomed and appreciated. If you're interested in improving ``xeofs`` or fixing issues, please open a Github issue_.

License
-------

This project is licensed under the terms of the MIT license.

Contact
-------

For questions or support, please open a Github issue_.



.. _issue: https://github.com/nicrie/xeofs/issues
.. _documentation: https://xeofs.readthedocs.io/en/latest/
.. _examples: https://xeofs.readthedocs.io/en/latest/auto_examples/index.html



Credits
----------------------

I want to acknowledge

- Andrew Dawson_, for his foundational Python package for EOF analysis.
- Yefee_, whose work provided useful references for implementing MCA in ``xeofs``.
- James Chapman_, creator of a Python package for Canonical Correlation Analysis.
- Diego Bueso_, for his open-source ROCK-PCA implementation in Matlab.
- The developers of NumPy_, pandas_, and xarray_ for their indispensable tools for scientific computations in Python.



.. _NumPy: https://www.numpy.org
.. _pandas: https://pandas.pydata.org
.. _xarray: https://xarray.pydata.org
.. _Chapman: https://github.com/jameschapman19/cca_zoo
.. _Bueso: https://github.com/DiegoBueso/ROCK-PCA
.. _Dawson: https://github.com/ajdawson/eofs
.. _Yefee: https://github.com/Yefee/xMCA


How to cite?
----------------------
Please make sure that when using ``xeofs`` you always cite the **original source** of the method used. Additionally, if you find ``xeofs`` useful for your research, you may cite it as follows::

   @software{rieger_xeofs_2023,
     title = {xeofs: Multi-dimensional {EOF} analysis and variants in xarray},
     url = {https://github.com/nicrie/xeofs}
     version = {1.0.0},
     author = {Rieger, Niclas},
     date = {2023},
     doi = {10.5281/zenodo.6323011}
   }
