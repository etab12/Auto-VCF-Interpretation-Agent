"""CrewAI tool: offline VCF quality-control metrics.
 
No network call - everything is computed from the file itself, so this is
cheap to run over a whole VCF before deciding whether to spend REST calls on
annotation.
"""
 
import json
 
from crewai.tools import tool
 
from tools.vcf_io import TRANSITIONS, parse_vcf_records
 
 
@tool("vcf_qc_stats")
def vcf_qc_stats(vcf_path: str, max_records: int = 200000) -> str:
    """Compute quality-control metrics for a VCF file without any network call.
 
    Returns JSON with: total variants read, SNV/indel/MNV counts, multi-allelic
    sites, transition/transversion ratio, FILTER value counts, PASS rate, QUAL
    distribution (min/p25/median/p75/max), per-chromosome counts, and
    missing-genotype rate.
 
    Args:
        vcf_path: Path to the .vcf or .vcf.gz file to summarise.
        max_records: Stop after this many variant records (memory guard).
    """
    try:
        recs = parse_vcf_records(vcf_path, limit=max_records)
        if not recs:
            return "ERROR: no variant records parsed from %s" % vcf_path
 
        n = len(recs)
        filters, per_chrom, quals = {}, {}, []
        snv = indel = mnv = multiallelic = ti = tv = 0
        missing_gt = total_gt = 0
 
        for r in recs:
            filters[r["filter"]] = filters.get(r["filter"], 0) + 1
            per_chrom[r["chrom"]] = per_chrom.get(r["chrom"], 0) + 1
            if r["qual"] is not None:
                quals.append(r["qual"])
 
            alts = r["alt"].split(",")
            if len(alts) > 1:
                multiallelic += 1
            ref = r["ref"]
            for alt in alts:
                if len(ref) == 1 and len(alt) == 1:
                    snv += 1
                    if (ref.upper(), alt.upper()) in TRANSITIONS:
                        ti += 1
                    else:
                        tv += 1
                elif len(ref) == len(alt):
                    mnv += 1
                else:
                    indel += 1
 
            for gt_field in r["samples"].values():
                total_gt += 1
                if gt_field.split(":")[0] in ("./.", ".|.", "."):
                    missing_gt += 1
 
        quals.sort()
 
        def q(p):
            if not quals:
                return None
            return round(quals[min(int(len(quals) * p), len(quals) - 1)], 2)
 
        stats = {
            "file": str(vcf_path),
            "records_read": n,
            "truncated": n >= max_records,
            "variant_classes": {
                "snv": snv,
                "indel": indel,
                "mnv": mnv,
                "multiallelic_sites": multiallelic,
            },
            "ti_tv_ratio": round(float(ti) / tv, 3) if tv else None,
            "filters": filters,
            "pass_rate": round(
                (filters.get("PASS", 0) + filters.get(".", 0)) / float(n), 4
            ),
            "qual": {
                "n": len(quals),
                "min": round(quals[0], 2) if quals else None,
                "p25": q(0.25),
                "median": q(0.5),
                "p75": q(0.75),
                "max": round(quals[-1], 2) if quals else None,
            },
            "genotypes": {
                "fields": total_gt,
                "missing": missing_gt,
                "missing_rate": (
                    round(missing_gt / float(total_gt), 4) if total_gt else None
                ),
            },
            "chromosomes": dict(sorted(per_chrom.items(), key=lambda kv: -kv[1])),
        }
        return json.dumps(stats, indent=2, default=str)
 
    except Exception as exc:
        return "ERROR in vcf_qc_stats: %s: %s" % (type(exc).__name__, exc)