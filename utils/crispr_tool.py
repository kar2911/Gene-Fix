# utils/crispr_tool.py

def generate_repair_plan(gene, mutation):
    """
    Generates a basic CRISPR repair plan for the specified gene and mutation.
    
    Args:
    gene (str): The name of the gene (e.g., 'TP53', 'KRAS').
    mutation (str): The mutation in HGVS format (e.g., 'p.R175H', 'p.G12V').
    
    Returns:
    str: A string containing the CRISPR repair plan.
    """
    
    # Example logic for generating gRNA, PAM sequence, and ssODN based on mutation
    # (In a real implementation, integrate real CRISPR design tools like CRISPResso, CRISPOR, etc.)
    
    # Sample dummy values for gRNA, PAM, and ssODN
    gRNA = f"gRNA targeting sequence for {mutation}"
    pam_sequence = f"PAM sequence for {mutation} (e.g., NGG)"
    ssODN = f"ssODN template for {mutation} (single-stranded donor template for HDR)"
    
    # Example of how the repair plan could be structured.
    repair_plan = (
        f"CRISPR Repair Plan for Gene: {gene}\n"
        f"Mutation: {mutation}\n\n"
        f"1. Generate gRNA: {gRNA}\n"
        f"2. Design PAM: {pam_sequence}\n"
        f"3. Design ssODN for HDR (Homology-Directed Repair): {ssODN}\n"
        f"4. Validate off-target effects and specificity using CRISPR design tools.\n"
        f"5. Deliver CRISPR components (gRNA, Cas9, ssODN) into target cells.\n"
        f"6. Verify successful gene editing through sequencing."
    )
    
    # Return the generated CRISPR repair plan
    return repair_plan
