|Banner|

`Website <https://tatradev.com>`_
• `Docs <https://tatradev.com>`_
• `Blog <https://tatradev.com>`_
• `Twitter <https://tatradev.com>`_
• `Chat (Community & Support) <https://tatradev.com>`_
• `Tutorial <https://tatradev.com>`_

# TODO: add useful installation links, code coverage and test from CICD

[![Build Status](https://github.com/TatraDev/pipertool/workflows/test/badge.svg?branch=venv_logic&event=push)](https://github.com/TatraDev/pipertool/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/TatraDev/pipertool/branch/master/graph/badge.svg)](https://codecov.io/gh/TatraDev/pipertool)
[![Python Version](https://img.shields.io/pypi/pyversions/pipertool.svg)](https://pypi.org/project/pipertool/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

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


Snap (Snapcraft/Linux)
----------------------


Choco (Chocolatey/Windows)
--------------------------

Brew (Homebrew/Mac OS)
----------------------

Conda (Anaconda)
----------------

pip (PyPI)
----------

Comparison to related technologies
==================================

#. Data Engineering tools such as `AirFlow <https://airflow.apache.org/>`_,
   `Luigi <https://github.com/spotify/luigi>`_, and others - We use Airflow and Luigi as possible context for executors

#. Opyrator -

#. Ansible -

#. Kubernetes -

#. Dagster -

#. DVC, MLFlow, and others -

#.


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



.. |Banner| image:: https://tatradev.com
   :target: https://tatradev.com
   :alt: Piper logo


.. |Contribs| image:: https://tatradev.com
   :target: https://github.com/TatraDev/piper/graphs/contributors
   :alt: Contributors