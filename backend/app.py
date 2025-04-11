from flask import Flask, request, jsonify
from utils.mutation_parser import parse_mutation
from utils.crispr_tool import generate_repair_plan
from utils.clinical_trials import get_trials
from gene_data import GENE_DATA
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route('/gene-fix', methods=['GET','POST'])
def process_mutation():
    data = request.get_json()
    gene = data.get('gene')
    mutation = data.get('mutation')
    mut_type = data.get('mutation_type')
    
    # Parse the mutation
    parsed_mutation = parse_mutation(mutation)

    if 'error' in parsed_mutation:
        return jsonify({'error': parsed_mutation['error']}), 400

    parsed_mut_type = parsed_mutation['mutation_type']
    mutation_info = {
        'gene': gene,
        'mutation': mutation,
        'mut_type': parsed_mut_type,
        'mutation_details': parsed_mutation
    }
    
    wild_url = GENE_DATA['Gene'][gene]['wild']
    mutated_url = GENE_DATA['Gene'][gene][mutation]['Missense']

    # CRISPR repair plan and clinical trials
    repair_plan = generate_repair_plan(gene, mutation)
    trials = get_trials(gene)

    return jsonify({
        'gene': gene,
        'mutation': mutation,
        'mut_type': parsed_mut_type,
        'repair': repair_plan,
        'trials': trials,
        'mutation_info': mutation_info,
        'wild-url': wild_url,
        'mutated_url': mutated_url
        
    })

if __name__ == '__main__':
    print("Flask app is running...")
    app.run(debug=True)
