=========
irholiday
=========


.. image:: https://img.shields.io/pypi/v/irholiday.svg
        :target: https://pypi.python.org/pypi/irholiday

.. image:: https://img.shields.io/travis/hadi-gharibi/irholiday.svg
        :target: https://travis-ci.org/hadi-gharibi/irholiday

.. image:: https://readthedocs.org/projects/irholiday/badge/?version=latest
        :target: https://irholiday.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Installation
------------

::

    $ pip install irholiday

to install from the latest source use following command

::

    $ pip install git+git://github.com/hadi-gharibi/irholiday.git


Usage
------

Enter the start and end year! that all :D
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
that's all :D

.. code:: python

    from irholiday import irHoliday

    # initialise the class
    calendar = irHoliday()

    # export data on dataframe
    df = calender.to_df(1388,1392)

    # export data on csv
    calnder.to_csv(1388,1392,'path/to/data')

