from flask import Flask, render_template, request, jsonify
from flask_assets import Environment, Bundle

from spacy_pl_demo import (
    lemmatizer as lemmatizer_demo,
    vectors as vectors_demo,
)

app = Flask('spacy-pl-demo', static_folder='static')
assets = Environment(app)
bundles = {
    'css': Bundle(
        'src/uikit/css/uikit.css',
        output='build/styles.css',
        filters='cssmin'
    ),
    'js': Bundle(
        'src/uikit/js/uikit.js',
        'src/uikit/js/uikit-icons.js',
        'src/axios/axios.js',
        'src/main.js',
        output='build/bundle.js',
        # filters='jsmin'  # TODO: This does not handle template strings properly (whitespace is squashed)
    )
}
assets.register(bundles)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lemmatizer', methods=['POST'])
def lemmatizer():
    """
    Request schema: {'query': <list of words to search: str>}
    Response schema: [{'token_text': str, 'direct_match': bool, 'lemma_match': bool}]
    """
    if not request.is_json:
        return jsonify({}), 400
    query = request.json.get('query', '')
    print(f"query={repr(query)}")
    sp = lemmatizer_demo.SearchProcessor()
    search_results = sp.process_query(query)
    json_results = jsonify([sr._asdict() for sr in search_results])
    return json_results, 200


@app.route('/vectors', methods=['POST'])
def vectors():
    """
    Request schema: {'words': <list of words to search: str>}
    Response schema: {'td' <list of rows:<list of column values>>, 'th': <list of table column names>}
    """
    if not request.is_json:
        return jsonify({}), 400
    words = request.json.get('words', [])
    sc = vectors_demo.SimilarityCalculator()
    words, similarities = sc.calculate_pairwise_similarity(words)
    table_headers = ['word'] + words  # 1st column and header will contain words
    table_rows = [
        [word] + [f"{sim_val:0.2f}" for sim_val in similarity_row]
        for word, similarity_row in zip(words, similarities)
    ]
    return jsonify({
        'td': table_rows,
        'th': table_headers
    }), 200
