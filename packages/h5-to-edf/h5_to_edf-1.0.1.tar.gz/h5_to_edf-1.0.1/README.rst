
h5_to_edf is a tool developed at ESRF to convert a HDF5 file to EDF files.

Installation
~~~~~~~~~~~~

``pip install h5_to_edf``

How to use
~~~~~~~~~~

The converter needs the name of the hdf5 file to be converted, and the output directory where the EDF files will
be created.

``convert_to_edf "path/file_001.h5" output_directory``

You can also convert multiple hdf5 files at once with the following command:

``convert_to_edf "path/file_0*.h5" output_directory``