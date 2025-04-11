from flask import Flask, render_template, request
from utils.mutation_parser import parse_mutation
from utils.crispr_tool import generate_repair_plan
from utils.clinical_trials import get_trials  # API call to get clinical trials

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        gene = request.form['gene']
        mutation = request.form['mutation']
        mut_type = request.form['mutation_type']
        
        # Parse the mutation using the mutation_parser.py
        parsed_mutation = parse_mutation(mutation)
        
        # Check if the mutation format is valid
        if 'error' in parsed_mutation:
            return render_template('index.html', error=parsed_mutation['error'])
        
        # If mutation is valid, extract information
        parsed_mut_type = parsed_mutation['mutation_type']
        mutation_info = {
            'gene': gene,
            'mutation': mutation,
            'mut_type': parsed_mut_type,
            'mutation_details': parsed_mutation
        }
        
        # Fetching the CRISPR repair plan
        repair_plan = generate_repair_plan(gene, mutation)
        
        # Fetch clinical trials related to the gene
        trials = get_trials(gene)
        
        return render_template('result.html', gene=gene, mutation=mutation,
                               mut_type=parsed_mut_type, repair=repair_plan,
                               trials=trials, mutation_info=mutation_info)
    
    return render_template('index.html')


if __name__ == '__main__':
    print("Flask app is running...")
    app.run(debug=True)
