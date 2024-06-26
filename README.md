[![DOI](https://zenodo.org/badge/611882682.svg)](https://zenodo.org/doi/10.5281/zenodo.11190828)

# PADME Conductor Library

<p align="center">
    <img src="https://raw.githubusercontent.com/sawelt/padme-conductor/main/logo.svg" width=220>
</p>

A library to simplify the interactions with the Personal Health Train (PHT) and its Stations.


## Connection Parameters

When working with the Stations you typically want to retrieve the information of how to connect to the database first.
This can be done with the `get_environment_vars` function, by passing the variable keys which need to be retrieved.

```python
env = pc.get_environment_vars(
    [
        "DATA_SOURCE_USERNAME",
        "DATA_SOURCE_HOST",
        "DATA_SOURCE_PASSWORD",
        "DATA_SOURCE_PORT",
        "STATION_NAME",
    ]
)
```

## Database Plugins

The next step would be to use the connection parameters and query the database of the Station.
For that, we first instantiate a database plugin for the appropriate database type.

### SQL

```python
sql = SqlPlugin(
    db_name="patientdb",
    user=env["DATA_SOURCE_USERNAME"],
    password=env["DATA_SOURCE_PASSWORD"],
    host=env["DATA_SOURCE_HOST"],
    port=env["DATA_SOURCE_PORT"],
)
```

### FHIR

```python
fhir_plugin = FHIRClient(f"http://192.168.0.1:8080/fhir")
```


## Querying Databases

With the database plugin, we can query the data from the Station.
For that, we pass a default `Query` object and the current station name to the `query` function.

```python
result = pc.query(
    Query("SELECT * FROM patients WHERE age >= 50", sql_plugin))
```

If the queries for each station differ, you can pass a list of queries and the current station name instead:

```python
result = pc.query(
    [
        Query("SELECT * FROM patients WHERE age >= 50", sql, "Klee"),
        Query("SELECT * FROM patient_info WHERE age >= 50", sql, "Bruegel"),
    ],
    env["STATION_NAME"],
)
```

## Executing the Analysis

You can now design your analysis with the libraries and frameworks you like.
This analysis can be e.g. a Machine Learning model, you set up and train, or an analysis that collects statistical data.

To execute the analysis we then pass the analysis function to the `execute_analysis` function, with all the parameters your function expects.

```python
def my_analysis(query_result):
    res = len(query_result)
    pc.log(f"found {res} patients")
    return res

res = pc.execute_analysis(my_analysis, result)
```

## Saving the Results

We can then save the results from our analysis in the Train file system.
To simplify this Train interaction we provide the `save` function.

You can separate the saved results, either by each run, each station, or not separate them.
The append parameter defines whether the content should be appended to the file or not.


```python
save_string = f"The result is {res}"
pc.save(save_string, "result.txt", separate_by=Separation.STATION, append=True)
```

## Retrieving Previous Results

To retrieve the previous results, like a previous state of a machine learning model, you can use the `retrieve_prev_result` function.

*If you have separated your results when saving, you also need to provide the separation strategy when retrieving.*

```python
prev = pc.retrieve_prev_result("result.txt", separate_by=Separation.STATION)
```

## Logging

You can use the `log` functions to log simultaneously to stdout/stderr and a log file in the Train file system.
We also provide the ability to add custom tags to a log function with the `extra` parameter.

```python
pc.log("hello world", extra={"tags": ["cpu_consumption"]})

pc.log_debug("hello world")
pc.log_info("hello world")
pc.log_warning("hello world")
pc.log_error("hello world")
pc.log_critical("hello world")
```


## Simple example

This is a simple example Train-analysis showing the concepts described above.

```python
import padme_conductor as pc
from padme_conductor import Query, Separation
from padme_conductor.Plugins.SQL import SqlPlugin

env = pc.get_environment_vars(
    [
        "DATA_SOURCE_USERNAME",
        "DATA_SOURCE_HOST",
        "DATA_SOURCE_PASSWORD",
        "DATA_SOURCE_PORT",
        "STATION_NAME",
    ]
)

sql = SqlPlugin(
    db_name="patientdb",
    user=env["DATA_SOURCE_USERNAME"],
    password=env["DATA_SOURCE_PASSWORD"],
    host=env["DATA_SOURCE_HOST"],
    port=env["DATA_SOURCE_PORT"],
)

result = pc.query(
    [
        Query("SELECT * FROM patients WHERE age >= 50", sql, "Klee"),
        Query("SELECT * FROM patient_info WHERE age >= 50", sql, "Bruegel"),
    ],
    env["STATION_NAME"],
)


def analysis(query_result):
    res = len(query_result)
    pc.log(f"found {res} patients")
    return res


res = pc.execute_analysis(analysis, result)
prev = pc.retrieve_prev_result("result.txt", separate_by=Separation.STATION)
pc.log(prev, extra={"tags": ["cpu_consumption"]})


# Write to file
save_string = env["STATION_NAME"] + ":" + str(res) + "\n"
pc.save(save_string, "result.txt", separate_by=Separation.STATION)

```
