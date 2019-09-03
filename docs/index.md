# kopylog

*Your log companion for algorithms structuration*

[![Python versions](https://img.shields.io/pypi/pyversions/kopylog.svg)](https://pypi.python.org/pypi/kopylog/) [![Build Status](https://travis-ci.org/smarie/python-kopylog.svg?branch=master)](https://travis-ci.org/smarie/python-kopylog) [![Tests Status](https://smarie.github.io/python-kopylog/junit/junit-badge.svg?dummy=8484744)](https://smarie.github.io/python-kopylog/junit/report.html) [![codecov](https://codecov.io/gh/smarie/python-kopylog/branch/master/graph/badge.svg)](https://codecov.io/gh/smarie/python-kopylog)

[![Documentation](https://img.shields.io/badge/doc-latest-blue.svg)](https://smarie.github.io/python-kopylog/) [![PyPI](https://img.shields.io/pypi/v/kopylog.svg)](https://pypi.python.org/pypi/kopylog/) [![Downloads](https://pepy.tech/badge/kopylog)](https://pepy.tech/project/kopylog) [![Downloads per week](https://pepy.tech/badge/kopylog/week)](https://pepy.tech/project/kopylog) [![GitHub stars](https://img.shields.io/github/stars/smarie/python-kopylog.svg)](https://github.com/smarie/python-kopylog/stargazers)

In many data science projects, and some general-purpose software projects as well, we create "master" functions that, when executed, execute several steps sequentially or in parallel. These steps might 

 - *take a significant amount of time*, in which case a common need is to quickly understand which step takes the most time (before going to a dedicated profiling tool)
 
 - *log a significant number of message*, in which case it becomes important to be able to structure the log
 
 - *generate a number of intermediate results* that could be useful for example to debug an issue that happened in production. Usually these intermediate results are not part of your API, their number and nature changes often with your code version and therefore you do not wish to create a specific new output to the functions just to gather them.


For large scale projects requiring complex pipelines, parallelism support and distributed execution platforms (e.g. Hadoop), dedicated frameworks exist such as [Spotify Luigi](https://github.com/spotify/luigi) or [Apache Airflow](https://github.com/apache/airflow). These frameworks provide most of the above, and much more. But for tiny projects where you just wish to organize your code in a few "steps" there does not seem to be anything out there, that's why `kopylog` exists.


## Installing

```bash
> pip install kopylog
```

## Usage

### Basic

```python

```

## Main features / benefits

**TODO**

## See Also

**TODO**

### Others

*Do you like this library ? You might also like [my other python libraries](https://github.com/smarie/OVERVIEW#python)* 

## Want to contribute ?

Details on the github page: [https://github.com/smarie/python-kopylog](https://github.com/smarie/python-kopylog)
