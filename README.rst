AnalyzeEmporia
==============

A simple script to analyze data exported from Emporia to look for trends.

Getting the data
----------------

First you need to obtain the data to analyze.
Head to `Emporia's partner site <https://partner.emporiaenergy.com/>`__ and log in.
Then at the top of the page using the "Filter by status" drop down, select
"Online". Then click the checkbox in the upper left of the table, in the header
row, in order to select all online meters. Click the "Export Data" data button
in the top right of the page. A menu will pop up - select "Hourly Data" -> "All Available"
then "Mains", then for Column Headers, select either option. Click "Start".

When the file finishes downloading, extract the CSV from the ZIP file
(it should be called `Hours.csv`) and drop it in this directory.

Setting up the environment
--------------------------

You must create a python virtual environment and install the dependencies (replace
$this_dir with the directory in which this file resides):

.. code:: bash

    cd $this_dir
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt

Analyzing the data
------------------

To analyze the data, just run `./main.py $days` while inside of this directory, replacing
$days with the number of days to analyze. (You must have your virtual environment activated.
If you just ran the install it will be - if not, you must run `source venv/bin/activate` first.)

Choosing 1 day would mean the first day usage for each individual meter would be
compared against the 2nd day usage.

Choosing 365 days would compare the first year's worth of data from each meter against
the second year's worth of data, and so on.

Since meters come online throughout the year, the data is per-meter, not per year.
So choosing 365 days doesn't analyze last year versus this year, it analyzes
first versus second year of meter install.

scipy's `ttest_ind <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html>`__
is used to perform the statistical significance test.
