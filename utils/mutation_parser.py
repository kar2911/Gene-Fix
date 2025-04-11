import re

def parse_mutation(mutation):
    """
    Parse the mutation string in HGVS format and extract relevant details.
    
    Args:
    mutation (str): Mutation in HGVS format (e.g., p.R175H, c.5382insC)
    
    Returns:
    dict: Parsed mutation information containing details about type, position, and variant.
    """
    # Pattern for matching HGVS format (e.g., p.R175H, c.5382insC)
    mutation_patterns = {
        "missense": r"^p\.(\w+)(\d+)(\w+)$",  # p.R175H or p.G12V
        "nonsense": r"^p\.(\w+)(\d+)(\*|\?|\$)$",  # p.R175* or p.G12$
        "insertion": r"^c\.(\d+)ins([A-Za-z0-9]+)$",  # c.5382insC
        "deletion": r"^c\.(\d+)del([A-Za-z0-9]+)$"  # c.5382delA
    }

    parsed_data = {}

    # Try matching against different mutation patterns
    for mut_type, pattern in mutation_patterns.items():
        match = re.match(pattern, mutation)
        if match:
            parsed_data['mutation_type'] = mut_type
            if mut_type == "missense" or mut_type == "nonsense":
                parsed_data['amino_acid'] = match.group(1)
                parsed_data['position'] = match.group(2)
                parsed_data['new_amino_acid'] = match.group(3)
            elif mut_type == "insertion":
                parsed_data['position'] = match.group(1)
                parsed_data['inserted_sequence'] = match.group(2)
            elif mut_type == "deletion":
                parsed_data['position'] = match.group(1)
                parsed_data['deleted_sequence'] = match.group(2)
            return parsed_data
    
    # If no pattern matches, return an error message
    return {"error": "Invalid HGVS mutation format"}
