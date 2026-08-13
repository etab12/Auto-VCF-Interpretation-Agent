import requests

from crewai.tools import tool


@tool("Search PubMed")
def search_pubmed(query: str, max_results: int = 5) -> str:
    """
    Search PubMed for scientific papers related to a gene or genomic variant.
    """

    # Step 1: Search PubMed and get PMIDs
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }

    search_response = requests.get(
        search_url,
        params=search_params,
        timeout=15,
    )

    search_response.raise_for_status()

    search_data = search_response.json()

    pmids = search_data.get("esearchresult", {}).get("idlist", [])

    if not pmids:
        return f"No PubMed results found for: {query}"

    # Step 2: Get information about those PMIDs
    summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    summary_params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
    }

    summary_response = requests.get(
        summary_url,
        params=summary_params,
        timeout=15,
    )

    summary_response.raise_for_status()

    summary_data = summary_response.json()

    papers = []

    for pmid in pmids:
        paper = summary_data.get("result", {}).get(pmid, {})

        title = paper.get("title", "Unknown title")
        journal = paper.get("fulljournalname", "Unknown journal")
        pubdate = paper.get("pubdate", "Unknown date")

        papers.append(
            f"""
Title: {title}
PMID: {pmid}
Journal: {journal}
Publication Date: {pubdate}
PubMed: https://pubmed.ncbi.nlm.nih.gov/{pmid}/
"""
        )

    return "\n".join(papers)


@tool("Lookup ClinVar Variant")
def lookup_clinvar_variant(variation_id: str) -> str:
    """
    Look up a genomic variant in ClinVar by its Variation ID.
    Returns the gene, clinical significance, and directly associated disease.
    Use the SOURCE_ID from the VCF INFO field as the variation_id input.
    """

    variation_id = str(variation_id).strip()

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "clinvar",
        "id": variation_id,
        "retmode": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        return f"ClinVar lookup failed: {exc}"
    except ValueError as exc:
        return f"ClinVar response parse failed: {exc}"

    record = data.get("result", {}).get(variation_id, {})
    if not record:
        return f"No ClinVar result found for Variation ID: {variation_id}"

    genes = [g.get("symbol", "?") for g in record.get("genes", [])]

    # germline_classification is the correct field in the current ClinVar API
    germline = record.get("germline_classification", {})
    significance = germline.get("description", "Unknown")
    review_status = germline.get("review_status", "Unknown")
    diseases = [
        t.get("trait_name", "")
        for t in germline.get("trait_set", [])
        if t.get("trait_name", "")
    ]

    return (
        f"CLINVAR RESULT\n"
        f"Variation ID    : {variation_id}\n"
        f"Accession       : {record.get('accession', 'Unknown')}\n"
        f"Variant title   : {record.get('title', 'Unknown')}\n"
        f"Gene(s)         : {', '.join(genes) or 'Unknown'}\n"
        f"Significance    : {significance}\n"
        f"Review status   : {review_status}\n"
        f"Associated disease(s): {'; '.join(diseases) or 'None listed'}\n"
        f"ClinVar link    : https://www.ncbi.nlm.nih.gov/clinvar/variation/{variation_id}/"
    )


if __name__ == "__main__":
    result = search_pubmed.run(query="BRCA1", max_results=3)
    print(result)
    