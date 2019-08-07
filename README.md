This library provides the functionality of the [esa_ttn](https://github.com/collide-uni-due/esa_ttn) library
as a webservice. Installing esa_ttn is a prerequisite to running this webservice.

A second requirement is an ESA database for the language you want to use the service with.
Ready made datasets can be found [here](https://github.com/collide-uni-due/esa_db)

To start the web service simply execute the app.py file
with the location of your ESA database as the first parameter and the language
of the ESA db as a second parameter
```
python app.py ~/path/to/esa.db
```

The service will then be available on the port 5000 under '/get_network/'
If you wanted to use the service locally you would call
```
127.0.0.1:5000/get_network/
```

The endpoint expects a json object of the following structure,
 with the shown default values:

```json
{
    "text": "Text to be turned into a network",
    "score_shreshold": 5000,
    "connecting_concepts": false,
    "map_tokens_to": "articles",
    "window_size": 20,
    "filter_network": false,
    "filter_type": "core",
    "filter_threshold": 2,
}
```

- **text**: The text to turn into a network
- **score_shreshold**: The algorithm uses a score threshold for the score
which is used to make connections between concepts that both have a value set at
a certain vector dimension. If two concepts both have a non zero value for a dimensions
(Ex.: "Psychology"), their values are multiplied together to calculate a score. If the
score exceeds the threshold a connection between the concepts is made in the network
- **connecting concepts** Should connecting concepts (the labels for the dimensions of the
ESA vectors) be part of the network, or should there be only direct connections between
concepts from the input text.
- **map_tokens_to**: Possible values are "articles" or "terms". If the tokens of the input text
are mapped to articles then the dimensions of the ESA vectors for these tokens
are terms and vice versa. The type of this paramater is the type of the nodes in the
resulting network.
- **window_size**: The size of the sliding window that moves over the text. Connections between
concepts are only possible if they appear together in the window. The bigger this is,
the more likely there are connections between concepts that are far apart in the text
- **filter_network**: Since there might be some noise in creating the nodes and connections between terms,
it is possible to add an extra filtering step for the network. The other filter parameters are only
relevant if this is set to true.
- **filter_type**: What node measure to use for filtering the network.
Possible values are "eigenvector", "betweenness", "degree", "core". The first three are
centrality meeasures. The last one is the highest k-core a node is part of.
- **filter_threshold**: Value of the measure chosen in *filter_type*. Any node that has a value
below this threshold is deleted from the network.

The service returns a json object of the form:

```json
{
  "text_possible_edge_list": [["token_a", "token_b", "connecting_concept", 6547]],
  "network": {...}
}
```

The field **text_possible_edge_list** containts a list of rows each describing a possible
edge in the network. At this point no score threshold is applied yet. If
the network is empty or very sparce you can look into this list and 
adjust your score threshold accordlingly.

THe field *network* is the generated network for the input text. It is in the format
of node-link data as used by [D3JS](https://www.d3-graph-gallery.com/network):

```json
{ "nodes": [
  { "id": 1, "name": "A" },
  { "id": 2, "name": "B" }
],
"links": [
  { "source": 1, "target": 2 }
]}
```

With extra node/edge attributes added as key/value pairs to the nodes/links obects.
