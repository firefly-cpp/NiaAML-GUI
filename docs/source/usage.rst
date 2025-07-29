Usage
=====

To run the GUI, first install the package via pip or from source:

.. code-block:: bash

   pip install niaaml-gui

Then run:

.. code-block:: bash

   poetry run niaaml-gui

The GUI allows you to build and optimize machine learning pipelines visually by dragging and connecting blocks.

Components
----------

- **Data input**: Select a CSV file and define the output folder.
- **Preprocessing**: Includes encoders and imputers.
- **Feature Engineering**: Feature selection and transform blocks.
- **Modeling**: Classifiers and optimization algorithms.
- **Fitness Function**: Determines the pipeline’s quality.
