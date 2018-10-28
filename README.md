# pygrakn

A simplified interface built on top of the official grakn-python client.

## Features

- Less code / boilerplate.
- Query results served as primitives (python lists / dicts etc.). Thus more immediately intelligble, accessable, and JSON-serialisable.
- Some added conveniences such as match_or_insert function
- Still access underlying grakn objects if necessary

## Usage

python`
import pygrakn.pygrakn as grakn

with grakn.Graph(uri='myuri', keyspace='mykeyspace') as graph:
    response = graph.execute('insert $x isa animal has name \"squirrel\"';)  # Escape your double quotes
    response = match.execute('match $x isa animal; get;')
    graph.commit()  # Commit changes. N.B. this also closes the session
`

ADD API PARAMS HERE

## Requirements

official python-grakn client:

`pip install grakn`

Grakn running.

## Contribution

Welcomed.



