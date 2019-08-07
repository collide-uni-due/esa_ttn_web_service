import sys
import pathlib as pl
from flask import Flask, request, jsonify
import esa_ttn
from networkx.readwrite.json_graph import node_link_data

app = Flask(__name__)

default_params = {
    "text": "Text to be turned into a network",
    "lang": "english",
    "score_shreshold": 5000,
    "connecting_concepts": False,
    "map_tokens_to": "articles",
    "window_size": 20,
    "filter_network": False,
    "filter_type": "core",
    "filter_threshold": 2,
}


@app.route('/get_network/')
def get_network():
    r_json = request.get_json(force=True)
    params = {**default_params, **r_json}
    text = params["text"]
    score_threshold = params["score_shreshold"]
    window_size = params["window_size"]
    connecting_concepts = params["connecting_concepts"]
    filter_network = params["filter_network"]
    map_tokens_to = params["map_tokens_to"]
    filter_type = params["filter_type"]
    filter_shreshold = params["filter_threshold"]
    if connecting_concepts:
        mode = "connecting_concepts"
    else:
        mode = "direction_connection"

    text_tokens = esa_ttn.text_to_tokens(text, lang)
    edge_df = esa_ttn.text_to_network_table(text_tokens, esa_db, window_size=window_size, map_tokens_to=map_tokens_to)
    concept_network = esa_ttn.edge_df_to_network(edge_df, score_cutoff=score_threshold, mode=mode)

    if filter_network:
        concept_network = esa_ttn.filter_network_by(concept_network, type=filter_type, cutoff_score=filter_shreshold)

    edge_df_list = [list(row) for i, row in edge_df.iterrows()]
    network_json_data = node_link_data(concept_network)
    result = {
        "text_possible_edge_list": edge_df_list,
        "network": network_json_data,
    }

    return jsonify(result)


if __name__ == '__main__':
    esa_db_path = pl.Path(sys.argv[1]).expanduser()
    lang = sys.argv[2]
    esa_db = esa_ttn.ESA_DB(str(esa_db_path))

    app.run()
