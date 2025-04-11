# utils/crispr_tool.py

def generate_repair_plan(gene, mutation):
    """
    Generates a biologically consistent and deterministic CRISPR repair plan
    for the specified gene and mutation.

    Args:
    gene (str): The name of the gene (e.g., 'TP53', 'KRAS').
    mutation (str): The mutation in HGVS protein format (e.g., 'p.R175H').

    Returns:
    str: A string containing the CRISPR repair plan.
    """

    # Predefined CRISPR design per gene
    gene_data = {
        "TP53": {
            "enzyme": "SpCas9",
            "pam": "NGG",
            "gRNA": "CAGGGCAGCTACGGTTTCCG",
            "remark": "Tumor suppressor gene – off-target effects must be minimized.",
        },
        "KRAS": {
            "enzyme": "SaCas9",
            "pam": "NNGRRT",
            "gRNA": "GTTGGAGCTGGTGGCGTAGG",
            "remark": "Focus on exon 2 targeting for G12 variants.",
        },
        "BRCA1": {
            "enzyme": "AsCas12a",
            "pam": "TTTV",
            "gRNA": "TTTGAGCTGCTTCTCAGTTC",
            "remark": "Used for correcting pathogenic variants in breast/ovarian cancers.",
        },
        "BRCA2": {
            "enzyme": "LbCas12a",
            "pam": "TTTV",
            "gRNA": "TTTCTCTGAGATAGGTCACC",
            "remark": "HDR with long homology arms preferred.",
        },
        "EGFR": {
            "enzyme": "SpCas9-HF1",
            "pam": "NGG",
            "gRNA": "AGGAGCTGTTCGGAATCCCA",
            "remark": "Target known hotspots like exon 19 or 21 in lung cancer.",
        },
    }

    default_data = {
        "enzyme": "SpCas9",
        "pam": "NGG",
        "gRNA": "GCTGAGTCCGTGACCTGTTG",
        "remark": "Generic CRISPR repair strategy. Gene-specific tools recommended.",
    }

    gene_info = gene_data.get(gene.upper(), default_data)

    # Infer mutation type
    if "fs" in mutation.lower() or "frameshift" in mutation.lower():
        mutation_type = "Frameshift"
        strategy = "Prime Editing"
        ssODN = f"Design pegRNA to correct frameshift caused by {mutation}"
    elif "*" in mutation or "X" in mutation.upper():
        mutation_type = "Nonsense"
        strategy = "HDR"
        ssODN = f"ssODN to restore codon lost in {mutation} nonsense mutation"
    elif "del" in mutation.lower():
        mutation_type = "Deletion"
        strategy = "HDR or NHEJ"
        ssODN = f"ssODN to reinsert deleted bases at {mutation}"
    elif "ins" in mutation.lower():
        mutation_type = "Insertion"
        strategy = "HDR"
        ssODN = f"ssODN to remove inserted sequence from {mutation}"
    elif ">" in mutation or mutation.startswith("p."):
        mutation_type = "Missense"
        strategy = "HDR"
        ssODN = f"ssODN to correct the missense mutation {mutation}"
    else:
        mutation_type = "Unknown"
        strategy = "HDR"
        ssODN = f"ssODN designed based on sequence flanking {mutation}"

    # Build the repair plan
    repair_plan = (
        f"🧬 CRISPR Repair Plan for Gene: {gene.upper()}\n"
        f"🔬 Mutation: {mutation} ({mutation_type})\n\n"
        f"1. Enzyme: {gene_info['enzyme']}\n"
        f"2. PAM Sequence: {gene_info['pam']}\n"
        f"3. gRNA: {gene_info['gRNA']}\n"
        f"4. Editing Strategy: {strategy}\n"
        f"5. ssODN / pegRNA: {ssODN}\n"
        f"6. Validation: Sequence the edited locus to confirm correction.\n"
        f"7. Note: {gene_info['remark']}"
    )

    return repair_plan