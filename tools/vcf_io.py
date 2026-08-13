"""Shared VCF parsing utilities used by qc_tool and vep_tool."""

import gzip

# SNV transitions (purine<->purine, pyrimidine<->pyrimidine)
TRANSITIONS = frozenset({
    ("A", "G"), ("G", "A"),
    ("C", "T"), ("T", "C"),
})


def _open(path):
    """Open a plain or gzipped VCF as text."""
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "rt", encoding="utf-8", errors="replace")


def parse_vcf_records(path, limit=200000):
    """
    Parse a VCF file and return a list of dicts with keys:
      chrom, pos, id, ref, alt, qual, filter, info, samples
    """
    records = []
    sample_names = []

    with _open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")

            if line.startswith("##"):
                continue

            if line.startswith("#CHROM"):
                parts = line.lstrip("#").split("\t")
                sample_names = parts[9:] if len(parts) > 9 else []
                continue

            parts = line.split("\t")
            if len(parts) < 8:
                continue

            chrom, pos, vid, ref, alt = parts[0], parts[1], parts[2], parts[3], parts[4]
            qual_str = parts[5]
            filt = parts[6]

            qual = None
            try:
                qual = float(qual_str)
            except (ValueError, TypeError):
                pass

            samples = {}
            if len(parts) > 9 and sample_names:
                for name, value in zip(sample_names, parts[9:]):
                    samples[name] = value

            records.append({
                "chrom": chrom,
                "pos": int(pos) if pos.isdigit() else pos,
                "id": vid,
                "ref": ref,
                "alt": alt,
                "qual": qual,
                "filter": filt,
                "info": parts[7] if len(parts) > 7 else ".",
                "samples": samples,
            })

            if len(records) >= limit:
                break

    return records


def record_to_vep_region(record):
    """
    Convert a parsed VCF record dict to the Ensembl VEP region string format.
    """
    chrom = record["chrom"]
    pos = record["pos"]
    ref = record["ref"]
    alt = record["alt"].split(",")[0]
    end = int(pos) + max(len(ref) - 1, 0)
    return "%s:%s-%s:1/%s" % (chrom, pos, end, alt)


def chunks(lst, size):
    """Yield successive sub-lists of length `size`."""
    for i in range(0, len(lst), size):
        yield lst[i: i + size]
