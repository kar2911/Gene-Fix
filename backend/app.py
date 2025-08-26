from flask import Flask, request, jsonify, send_from_directory
from utils.mutation_parser import parse_mutation
from utils.crispr_tool import generate_repair_plan
from utils.clinical_trials import get_trials
from utils.ai_helper import get_ai_simulation_message
from flask_cors import CORS, cross_origin
from gene_data import GENE_DATA

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Enhanced CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
        "supports_credentials": True
    }
})
@app.route('/static/<path:filename>')
@cross_origin(origins=["http://localhost:5173"])
def serve_static(filename):
    try:
        # Adjust this path to where your PDB files are stored
        static_folder = 'static'  # or '/path/to/your/static/files'
        return send_from_directory(static_folder, filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/gene-fix', methods=['POST', 'OPTIONS'])
def process_mutation():
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    # Your existing POST logic
    data = request.get_json()
    
    gene = data.get('gene')
    mutation = data.get('mutation')
    mut_type = data.get('mutation_type')
    disease = data.get('disease_association')
    impact = data.get('mutation_impact')
    frequency = data.get('mutation_frequency')
    gene_function = data.get('gene_function')
    family_history = data.get('family_history')
    enzyme = data.get('enzyme')
    pam = data.get('pam')
    grna = data.get('grna')

    parsed_mutation = parse_mutation(mutation)
    if 'error' in parsed_mutation:
        return jsonify({'error': parsed_mutation['error']}), 400

    parsed_mut_type = parsed_mutation['mutation_type']
    repair_plan = generate_repair_plan(gene, mutation, enzyme, pam, grna)
    trials = get_trials(gene)
    
    wild_url = GENE_DATA['Gene'][gene]['wild']
    mutated_url = GENE_DATA['Gene'][gene][mutation][mut_type]
    
    prompt1 = f'''
        take all the elements that i will be giving you to, generate a live simulaton of cancer cell reprogramming such that it should be divided into 5 phases,each phase should contain description, risk factor, the success rate (out of 1-100%), what technology is used, what are the components are used for each step and at what amount. Use markdown formatting to structure your responses with headings, bullet points, and emphasis where appropriate.

        The following are the elements you should use:

        gene={gene}
        mutation={mutation}
        mut_type={parsed_mut_type}
        mutation_type={mut_type}
        disease={disease}
        impact={impact}
        frequency={frequency}
        gene_function={gene_function}
        family_history={family_history}
        enzyme={enzyme}
        pam={pam}
        grna={grna}
        '''
    ai_message = get_ai_simulation_message(prompt1)
    
    prompt2 = f'''
        generate me a summary of simulating the reprogramming of cancer cell into healthy cell in 1 para, also give required parameters of composition used in reprogramming based on the below characteristics of the cancer gene,Use markdown formatting to structure your responses with headings, bullet points, and emphasis where appropriate.

        gene={gene}
        mutation={mutation}
        mut_type={parsed_mut_type}
        mutation_type={mut_type}
        disease={disease}
        impact={impact}
        frequency={frequency}
        gene_function={gene_function}
        family_history={family_history}
        enzyme={enzyme}
        pam={pam}
        grna={grna}
    '''
    
    ai_message_2 = get_ai_simulation_message(prompt2)
    
    print(f'ai message 2: {ai_message_2}')

    return jsonify({
        'gene': gene,
        'mutation': mutation,
        'parsed_mut_type': parsed_mut_type,
        'mutation_type': mut_type,
        'disease': disease,
        'impact': impact,
        'frequency': frequency,
        'gene_function': gene_function,
        'family_history': family_history,
        'enzyme': enzyme,
        'pam': pam,
        'grna': grna,
        'repair': repair_plan,
        'trials': trials,
        'ai_response': ai_message,
        'ai_summary': ai_message_2,
        'wild_url': wild_url,
        'mutated_url': mutated_url
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)