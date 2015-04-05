urakata README
==================

Getting Started
---------------

::

 cd <directory containing this file>
 $VENV/bin/python setup.py develop
 $VENV/bin/urakata initialize development.ini
 $VENV/bin/pserve development.ini

sample
----------------------------------------

::

 $ urakata initialize development.ini
 $ urakata scan development.ini demo/season -overrides=demo/overrides.season.json > season.json
 $ urakata register development.ini season.json
 $ urakata codegen development.ini my-scaffold > scaffold.py


season.json

.. code-block:: bash

  $ python scaffold.py season
  autumn(default:):?
  aki
  month(default:):?
  gatsu
  INFO:__main__:emit[D] -- season
  INFO:__main__:emit[F] -- season/aki.txt
  spring(default:haru):?

  INFO:__main__:emit[F] -- season/haru.txt
  summer(default:natsu):?

  INFO:__main__:emit[F] -- season/natsu.txt
  winter(default:):?
  huyu
  INFO:__main__:emit[F] -- season/huyu.txt

.. code-block:: bash
 $ tree season
 season
 ├── aki.txt
 ├── haru.txt
 ├── huyu.txt
 └── natsu.txt

 0 directories, 4 files

 $ cat season/aki.txt

  aki
  - 9gatsu
  - 10gatsu
  - 11gatsu

