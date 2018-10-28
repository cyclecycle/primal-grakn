# pygrakn

A simplified interface to [grakn](https://grakn.ai/) built on top of the official [grakn-python client](https://github.com/graknlabs/grakn/tree/master/client-python).

## Features

- Less code / boilerplate.
- Query results served as primitives (python lists / dicts etc.). Thus more immediately intelligble, accessable, and JSON-serialisable.
- Some added conveniences such as match_or_insert function.
- Still access underlying grakn objects if necessary.

## Usage

### Example

```python
import pygrakn.pygrakn as grakn

with grakn.Graph(uri='myuri', keyspace='mykeyspace') as graph:
    query = 'insert $a isa animal has name \"squirrel\";'  # Escape your quotes, or use a raw string
    response = graph.execute(query)
    response = match.execute('match $a isa animal; get;')
    graph.commit()  # Commit changes. N.B. this also closes the session
```

### API

Name | Type | Description | Params
--- | --- |--- | ---
grakn.Graph | Class | Initiates the session. | uri, keyspace
grakn.Graph.execute | Method | Executes a query. | graql query
grakn.Graph.commit | Method | Commits the changes and ends the session. |
grakn.Graph.match_or_insert | Method | Given a graql query string, match if it exists in the graph, or else insert it | graql query without a 'match' or 'insert' statement, e.g, '$a isa animal has name \\"squirrel\\"'.

## Requirements

- Grakn running.
- Official python-grakn client:

    `pip install grakn`


## Contribution

Welcome.



