# primal-grakn

A convenience wrapper around the official [grakn-python client](https://github.com/graknlabs/grakn/tree/master/client-python).

## Features

- Less code / boilerplate.
- Response data looks and acts like primitive data structures (python lists / dicts etc.). Thus more immediately intelligble, accessable, and JSON-serialisable.
- Some added conveniences such as match_or_insert function.
- Still access all underlying grakn-python client functionality where needed.

## Why

The [grakn-python client](https://github.com/graknlabs/grakn/tree/master/client-python) provides a complete and efficient object-oriented method of interaction with a Grakn instance. It can require a lot of code and recursion to get data. This extension aims to provide convenience through reducing code involved in connecting to Grakn and working with response data. It reflects a manner of working with Grakn through python that I have found to be preferrable.

## Usage

### Example

```python
import primal_grakn.primal_grakn as grakn

with grakn.Graph(uri='myuri', keyspace='mykeyspace') as graph:
    query = 'insert $a isa animal has name \"squirrel\";'  # Escape your quotes, or use a raw string
    concept_map = graph.execute('match $a isa animal; get;')
    print(concept_map)
        {'a': {
            'id': 'V4144',
            'type': 'animal',
            'base_type': 'entity',
            'attributes': [{
                'id': 'V4216',
                'label': 'name',
                'value': 'squirrel'
            }]
        }}
    print(concept_map.object)  # Get the underlying ConceptMap object
    print(concept_map['a'].object)  # Get the underlying Concept object
    graph.commit()  # Don't forget to commit changes if you make them. N.B. this also closes the session
```

### API

Name | Type | Description | Params | Example
--- | --- |--- | --- | ---
grakn.Graph | Class | Initiates the session. | <ul><li>**kwarg** : uri : *string* : Default='localhost:48555'</li><li>**kwarg** : keyspace : *string* : Default=None</li><li>**kwarg** : credentials : *dict* : Default={}</li></ul> |
grakn.Graph.execute | Method | Executes a query. | <ul><li>**arg** : query : *string*</li></ul> | execute('match $a isa animal')
grakn.Graph.commit | Method | Commits the changes and ends the session. | |
grakn.Graph.match_or_insert | Method | Given a graql query string, match if it exists in the graph, or else insert it. | <ul><li>**arg** : query : *string* : graql query without a prepended 'match' or 'insert' statement</li></ul> | match_or_insert('$a isa animal has name \\"squirrel\\";') 

### Installation

#### Clone the repo

```bash
git clone https://github.com/cyclecycle/pygrakn.git
```

#### Requirements

- Grakn running.
- Official python-grakn client:

    `pip install grakn`

## Contributions

Are welcome :)



