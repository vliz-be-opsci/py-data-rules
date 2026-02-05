# PyDataRules

PyDataRules is a framework to validate tabular data. The general concept is to define rules on a data model and evaluate those rules in each cell that is in scope. Rule violations are eventually made available in a report (json, csv, ...).

PyDataRules can be extended by implementing custom rules. For this, prior experience with Pandas is desired.

## Data Model

The DataModel is an abstract representation of the data files on disk. It consists of a list of table aliases, with each table alias in turn referring to a file path, schema, and read method (by default pd.read_csv). Several file types are supported by passing the appropriate pandas read method for each table alias. (TODO: guess read method based on file extension)

Schemas list the label, data type, nullability and whitespace policy for each column in the table. (TODO: make it possible to instantiate a Schema from a yaml file)

After applying the read method on the file path, tables are internally represented by Table objects, a subclass of the pandas DataFrame. The Table objects are accessed via the `table_dict` attribute defined on a DataModel.

## Rules
Some rules can be defined as functions in an external python file, these rules are explicit rules. Other rules are implicit, these are defined at runtime by the RuleEngine (e.g. datatype checks, missing values, whitespace trimming, ...)

Explicit rules can be written somewhat like this:

```{python}
def my_custom_rule(table_dict: dict) -> List[Violation]:
    violations = []
    table = table_dict["<my_table_alias>"]
    <do something with the table and generate Violation objects>
    <append Violation objects to the violations list>
    return violations
```

In general, Table objects can be retrieved via their alias from the `table_dict` (essentially returning a pd.DataFrame-like object) or iterated over by using `table_dict.values()`.


## RuleEngine
The RuleEngine is the object that effectively performs the data validation and generates a violation report. A DataModel and a list of Rules are required to instantiate an engine.


![](assets/PyDataRules.drawio.png)
