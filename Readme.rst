|Banner|


|License| |Release| |Docs| |Build status| |Contact| |Blog|

**Piper** is an **open-source** platform for data science and machine
learning prototyping. Concentrate only on your goals. Key features:

#. Simple **python contexts** experience. Helps to create and deploy pipelines. Does not depend on any proprietary online services.

#. Connect each module into a **pipeline**. Run it via docker or virtual environment. Then build whole **infrastructure** by using venv, Docker or Cloud.

#. Decreases routine and repetitive tasks. Speed up process **from idea to production**.

#. Well-tested and reproducible. Easily extendable by your own **Executor**.

**Piper** aims to help data-scientists and machine-learning developers to create and build full infrastructure for their projects.

.. contents:: **Contents**
  :backlinks: none

How Piper works
=============

|Flowchart|



Quick start
===========
Quick start pipertool package compose env
===========

In root directory project run command in terminal

- sudo -u root /bin/bash

- create and activate venv

- pip install -r requirements.txt

- in configuration.py rename for correctly path for new directory

- python setup.py install

- piper --env-type compose start

- 0.0.0.0:7585 - FastApi

- 0.0.0.0:9001 - Milvus Console (minioadmin/minioadmin)

- piper --env-type compose stop

- pip uninstall piper

Quick start pipertool package compose env
===========

In root directory project run command in terminal

- sudo -u root /bin/bash

- create and activate venv

- pip install -r requirements.txt

- in configuration.py rename for correctly path for new directory

- python main.py

- await click CTRL+C from compose env



Installation
============

pip (PyPI)
----------

.. code-block:: bash
  :caption: pip installation
    pip install pipertool

Comparison to related technologies
==================================

#. **Jupyter** - is the de facto experimental environment for most data scientists. However, it is desirable to write experimental code.

#. **Data Engineering tools such as** `AirFlow <https://airflow.apache.org/>`_ or
   `Luigi <https://github.com/spotify/luigi>`_ - These are very popular ML pipeline build tools. Airflow can be connected to a kubernetes cluster or collect tasks through a simple PythonOperator. The downside is that their functionality is generally limited on this, that is, they do not provide ML modules out of the box. Moreover, all developments will still have to be wrapped in a scheduler and this is not always a trivial task. However, we like them and we use Airflow and Luigi as possible context for executors.

#. **Azure ML / Amazon SageMaker / Google Cloud** - Cloud platforms really allow you to assemble an entire system from ready-made modules and put it into operation relatively quickly. Of the minuses: high cost, binding to a specific cloud, as well as small customization for specific business needs. For a large business, this is the most logical option - to build an ML infrastructure in the cloud. We also maintain cloud options as posible ways for the deployment step.

#. **DataRobot/Baseten** - They offer an interesting, but small set of ready-made modules. However, in Baseten, all integration is implied in the kubernetes cluster. This is not always convenient and necessary for Proof-of-Concept. Piper also provides an open-source framework in which you can build a truly customized pipeline from many modules. Basically, such companies either do not provide an open-source framework, or provide a very truncated set of modules for experiments, which limits the freedom, functionality, and applicability of these platforms. This is partly similar to the hub of models and datasets in huggingface.

#. **Mlflow / DVC** - There are also many excellent projects on the market for tracking experiments, serving and storing machine learning models. But they are increasingly utilitarian and do not directly help in the task of accelerating the construction of a machine learning MVP project. We plan to add integrations to Piper with the most popular frameworks for the needs of DS and ML specialists.


Contributing
============

|Maintainability| |Donate|

Contributions are welcome! Please see our `Contributing Guide <https://tatradev.com>`_ for more
details. Thanks to all our contributors!

|Contribs|

Mailing List
============



Copyright
=========

This project is distributed under the Apache license version 2.0 (see the LICENSE file in the project root).

By submitting a pull request to this project, you agree to license your contribution under the Apache license version
2.0 to this project.



.. |Banner| image:: https://static.tildacdn.com/tild3434-6665-4638-a432-626636353134/illistration.svg
   :target: http://pipertool.org/
   :alt: Piper logo


.. |Contribs| image:: https://tatradev.com
   :target: https://github.com/TatraDev/piper/graphs/contributors
   :alt: Contributors


.. |Release| image:: https://img.shields.io/github/release/zifter/numeral-system-py.svg
   :target: https://github.com/TatraDev/pipertool/releases

.. |Build status| image:: https://github.com/TatraDev/pipertool/workflows/test/badge.svg?branch=venv_logic&event=push
    :target: https://github.com/TatraDev/pipertool/actions?query=workflow%3Atest

.. |Contact| image:: https://img.shields.io/badge/telegram-write%20me-blue.svg
    :target:  https://t.me/pipertool

.. |Blog| image:: https://img.shields.io/badge/site-my%20blog-yellow.svg
    :target:  https://tatradev.com

.. |License| image:: https://img.shields.io/badge/License-Apache-yellow.svg
    :target:  https://www.apache.org/licenses/LICENSE-2.0

.. |Docs| image:: https://readthedocs.org/projects/numeral-system-py/badge/?version=latest&style=flat
    :target:  http://pipertool.org
