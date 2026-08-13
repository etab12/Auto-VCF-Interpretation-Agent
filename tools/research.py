import requests


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


if __name__ == "__main__":
    result = search_pubmed("BRCA1", 3)
    print(result)