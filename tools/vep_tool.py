 
import json
import os
import time
 
import requests
from crewai.tools import tool
 
from tools.vcf_io import chunks, parse_vcf_records, record_to_vep_region
 
# --------------------------------------------------------------------------- #
# Config - internal, not exposed to the agent
# --------------------------------------------------------------------------- #
 
VEP_SERVER = os.getenv("ENSEMBL_REST_SERVER", "https://rest.ensembl.org")
SPECIES = "homo_sapiens"      # part of the endpoint path, not a tool argument
BATCH_SIZE = 200              # hard cap on the Ensembl POST endpoint
REQUEST_TIMEOUT = 120
MAX_RETRIES = 5
SLEEP_BETWEEN_BATCHES = 0.4   # stay under the ~15 req/s limit
 
_TX_FIELDS = (
    "gene_symbol", "gene_id", "transcript_id", "consequence_terms", "impact",
    "biotype", "canonical", "mane_select", "hgvsc", "hgvsp", "exon", "intron",
    "sift_prediction", "sift_score", "polyphen_prediction", "polyphen_score",
)
 
 
# --------------------------------------------------------------------------- #
# REST client
# --------------------------------------------------------------------------- #
 
def post_vep(variants):
    """POST one batch (<=200 variants) to the VEP region endpoint."""
    url = "%s/vep/%s/region" % (VEP_SERVER, SPECIES)
    params = {
        "canonical": 1, "hgvs": 1, "symbol": 1, "numbers": 1, "mane": 1,
        "sift": "b", "polyphen": "b", "af": 1, "af_gnomade": 1,
        "variant_class": 1,
    }
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    body = json.dumps({"variants": variants})
 
    for attempt in range(1, MAX_RETRIES + 1):
        resp = requests.post(
            url, headers=headers, params=params, data=body,
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 429:
            time.sleep(float(resp.headers.get("Retry-After", 2 ** attempt)))
            continue
        if resp.status_code in (500, 502, 503, 504) and attempt < MAX_RETRIES:
            time.sleep(2 ** attempt)
            continue
        raise RuntimeError(
            "VEP REST error %s: %s" % (resp.status_code, resp.text[:500])
        )
    raise RuntimeError(
        "VEP REST failed after %d attempts (rate limited)." % MAX_RETRIES
    )
 
 
def flatten_entry(entry):
    """Reduce one VEP JSON entry to the MANE/canonical transcript only."""
    txs = entry.get("transcript_consequences") or []
    if txs:
        chosen = next(
            (t for t in txs if t.get("mane_select")),
            next((t for t in txs if t.get("canonical")), txs[0]),
        )
        txs_out = [{k: chosen.get(k) for k in _TX_FIELDS if k in chosen}]
    else:
        txs_out = []
 
    colocated = entry.get("colocated_variants") or []
    rsids = [c.get("id") for c in colocated
             if str(c.get("id", "")).startswith("rs")]
    freqs = next(
        (c.get("frequencies") for c in colocated if c.get("frequencies")), None
    )
 
    return {
        "input": entry.get("input"),
        "location": "%s:%s-%s" % (
            entry.get("seq_region_name"), entry.get("start"), entry.get("end"),
        ),
        "allele_string": entry.get("allele_string"),
        "variant_class": entry.get("variant_class"),
        "most_severe_consequence": entry.get("most_severe_consequence"),
        "rsids": rsids[:3],
        "frequencies": freqs,
        "transcripts": txs_out,
    }
 
 
# --------------------------------------------------------------------------- #
# Tool
# --------------------------------------------------------------------------- #
 
@tool("vep_annotate")
def vep_annotate(vcf_path: str, max_variants: int = 200) -> str:
    """Annotate the variants in a VCF file using the Ensembl VEP REST API.
 
    Accepts .vcf or .vcf.gz. Reads the file, converts each record to VEP
    region notation and submits them in batches, retrying on rate limits.
 
    Returns JSON containing: source_file, submitted, annotated, batch_errors,
    and a results list. Each result has location, allele_string, variant_class,
    most_severe_consequence, rsids, frequencies, and the MANE or canonical
    transcript with gene_symbol, transcript_id, hgvsc, hgvsp,
    consequence_terms, impact, exon, intron, sift_prediction and
    polyphen_prediction.
 
    Call this ONCE per file. It handles all batching internally.
 
    Args:
        vcf_path: Path to the .vcf.gz or .vcf file to annotate.
        max_variants: Maximum number of variants to annotate in this call.
    """
    try:
        recs = parse_vcf_records(vcf_path, limit=max_variants)
        if not recs:
            return "ERROR: no variant records parsed from %s" % vcf_path
 
        payload = [record_to_vep_region(r) for r in recs]
        annotated, errors = [], []
 
        for i, batch in enumerate(chunks(payload, BATCH_SIZE)):
            try:
                annotated.extend(flatten_entry(e) for e in post_vep(batch))
            except Exception as exc:      # keep partial results usable
                errors.append("batch %d: %s" % (i, exc))
            time.sleep(SLEEP_BETWEEN_BATCHES)
 
        return json.dumps({
            "source_file": str(vcf_path),
            "submitted": len(payload),
            "annotated": len(annotated),
            "batch_errors": errors,
            "results": annotated,
        }, indent=2, default=str)
 
    except Exception as exc:
        return "ERROR in vep_annotate: %s: %s" % (type(exc).__name__, exc)
 