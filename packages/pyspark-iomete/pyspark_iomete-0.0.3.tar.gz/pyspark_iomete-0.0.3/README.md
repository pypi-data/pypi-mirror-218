# Pyspark IOMETE Library

This library is providing a set of utility functions to speed up the development of pyspark applications.


## Installation

```bash
pip install pyspark-iomete
```


## Utility functions

### get_spark_logger

This function is returning a spark logger instance.

As you may know, spark is using log4j as a logging framework. This function is returning a spark logger instance that is using the log4j logger. Standard python logging is not working with pyspark. The following function get the spark logger instance and returns it.

Usage:
```python
from pyspark_iomete.utils import get_spark_logger
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# spark session and name will be used to create the logger
# both are optional
logger = get_spark_logger(spark=spark, name="my_custom_logger")

# spark session will be retrieved using SparkSession.getActiveSession() and name will be set to the current file name
logger = get_spark_logger()
```

## Test utility functions

### table_name_with_random_suffix

This function is returning a table name with a random suffix. This is useful for testing purposes.

Usage:
```python
from pyspark_iomete.test_utils import table_name_with_random_suffix

table_name = table_name_with_random_suffix("my_table")
```
 