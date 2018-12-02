# primal-grakn

A convenience wrapper around the official [grakn-python client](https://github.com/graknlabs/grakn/tree/master/client-python).

## Features

- Less code / boilerplate.
- Response data looks and acts like generic data structures (lists / dicts etc.). Thus more immediately intelligble, accessable, and JSON-serialisable.
- Some added conveniences such as match_or_insert and explanation parsing.
- Still access all underlying grakn-python client functionality where needed.

## Why

The [grakn-python client](https://github.com/graknlabs/grakn/tree/master/client-python) provides a complete and efficient object-oriented method of interaction with a Grakn instance. It can require a lot of code and recursion to get the data however. This extension aims to provide convenience through reducing code involved in connecting to Grakn and working with response data. It reflects a manner of working with Grakn through python that I have found to be preferrable.

## Usage

### Example

```python
import primal_grakn as grakn

with grakn.Graph(uri='myuri', keyspace='mykeyspace') as graph:
    query = 'insert $a isa animal has name \"squirrel\";'  # Escape your quotes, or use a raw string
    concept_map = graph.execute('match $a isa animal; get;')
    print(concept_map)
        [{'a': {
            'id': 'V4144',
            'type': 'animal',
            'base_type': 'entity',
            'attributes': [{
                'id': 'V4216',
                'label': 'name',
                'value': 'squirrel'
            }]
        }}]
    print(concept_map.object)  # Get the underlying ConceptMap object
    print(concept_map['a'].object)  # Get the underlying Concept object
    graph.commit()  # Don't forget to commit changes if you make them. N.B. this also closes the session
```

### API

#### primal_grakn.Graph

| Name | Type | Description | Params | Example |
| --- | --- |--- | --- | --- |
| Graph | Class | Initiates the session. | <ul><li>**kwarg** : uri : *string* : Default='localhost:48555'</li><li>**kwarg** : keyspace : *string* : Default=None</li><li>**kwarg** : credentials : *dict* : Default={}</li></ul> |
Graph.execute | Method | Executes a query. | <ul><li>**arg** : query : *string*</li></ul> | execute('match $a isa animal') |
| Graph.commit | Method | Commits the changes and ends the session. | |
| Graph.match_or_insert | Method | Given a graql query string, match if it exists in the graph, or else insert it. | <ul><li>**arg** : query : *string* : graql query without a prepended 'match' or 'insert' statement</li></ul> | match_or_insert('$a isa animal has name \\"squirrel\\";') 

#### primal_grakn.ConceptDict

Dictionary respresenation of a Grakn Concept object.

Name | Type | Description | Params | Example
| --- | --- | --- | --- | --- |
| ConceptDict.object | Grakn Concept object | Corresponding grakn-python object |  |  |

### An explanation about explanations

At the time of writing, the explanation data structures Grakn provides are undocumented. Briefly, the Grakn ConceptMap object exposes the set of facts as a tree. The top level of this tree includes the inferred facts from the response, and the compositional facts are nested within deeper levels. 

At present, we provide two ways to access these facts:

- `concept_map.explanation` - the explanation tree as it is exposed by grakn-python, parsed into the form of a python dictionary.
- `concept_map.flat_explanation` - where the tree is flattened into a list. I found this much more convenient for my purposes, as it meant I could filter the list for only the types of concepts I was interested in for my explanation, and then sort the list into the logical order (Grakn does not provide any ordering in its explanation output), without recursion.

If you don't need information about the depth of facts underlying the inferences in your response, use `.flat_explanation`. 

### Installation

#### Clone the repo

```bash
git clone https://github.com/cyclecycle/pygrakn.git
```

#### Requirements

- Grakn running.
- Official python-grakn client:

    `pip install grakn`

## Contributions and improvements

Are welcome :)

- The match_or_insert function could be improved to handle a broader number of cases. It's only set up for simple queries at the moment.



