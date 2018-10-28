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
    print(response)
        [{
            'id': 'V4144',
            'type': 'animal',
            'base_type': 'entity',
            'attributes': [{
                'id': 'V4216',
                'label': 'name',
                'value': 'squirrel'
            }]
        }]
    graph.commit()  # Don't forget to commit changes. N.B. this also closes the session
```

### API

Name | Type | Description | Params | Example
--- | --- |--- | --- | ---
grakn.Graph | Class | Initiates the session. | <ul><li>**kwarg** : uri : *string* : Default='localhost:48555'</li><li>**kwarg** : keyspace : *string* : Default=None</li><li>**kwarg** : credentials : *dict* : Default={}</li></ul> |
grakn.Graph.execute | Method | Executes a query. | <ul><li>**arg** : query : *string*</li><li>**kwarg** : grakn_objs : *boolean* : includes the underlying grakn object in the results : Default=False</li></ul> | execute('match $a isa animal', grakn_objs=True)
grakn.Graph.commit | Method | Commits the changes and ends the session. | |
grakn.Graph.match_or_insert | Method | Given a graql query string, match if it exists in the graph, or else insert it | <ul><li>**arg** : query : *string* : graql query without a prepended 'match' or 'insert' statement</li></ul> | match_or_insert('$a isa animal has name \\"squirrel\\";') 

### Installation

#### Clone the repo

```bash
git clone https://github.com/cyclecycle/pygrakn.git
```

#### Requirements

- Grakn running.
- Official python-grakn client:

    `pip install grakn`

## Contribution

Welcome.



