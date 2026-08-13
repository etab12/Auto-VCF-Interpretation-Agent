import gzip
import json
import os
 
from crewai.tools import tool
 
REQUIRED_COLUMNS = [
    "CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO",
]
 
VALID_BASES = set("ACGTN*.")
 
 
def _reader(path):
    """Open plain or gzipped VCF as text, raising a clear error on corruption."""
    if str(path).endswith(".gz"):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "rt", encoding="utf-8", errors="replace")
 
 
@tool("validate_vcf_file")
def validate_vcf_file(vcf_path: str, max_malformed_examples: int = 5) -> str:
    """Check that a VCF file is readable and structurally valid before analysis.
 
    Accepts .vcf or .vcf.gz. Verifies that the file exists and is non-empty,
    that gzip content decompresses, that the ##fileformat header is present,
    that the #CHROM header line exists with the eight mandatory columns, and
    that data records parse. Counts records, sample columns and malformed
    lines, and reports the chromosome naming style.
 
    Returns JSON with: status (VALID, VALID_WITH_WARNINGS or INVALID), errors,
    warnings, and a details block. Run this before vcf_qc_stats or
    vep_annotate - if status is INVALID, no further analysis is meaningful.
 
    Args:
        vcf_path: Path to the .vcf.gz or .vcf file to validate.
        max_malformed_examples: How many bad lines to quote in the output.
    """
    errors = []
    warnings = []
    details = {
        "file": str(vcf_path),
        "compressed": str(vcf_path).endswith(".gz"),
        "size_bytes": None,
        "fileformat": None,
        "meta_lines": 0,
        "contig_lines": 0,
        "has_chrom_header": False,
        "sample_count": 0,
        "samples": [],
        "record_count": 0,
        "malformed_lines": 0,
        "malformed_examples": [],
        "chrom_naming": None,
        "distinct_chromosomes": 0,
    }
 
    # ---- existence and size -------------------------------------------- #
    if not os.path.exists(vcf_path):
        return json.dumps({
            "status": "INVALID",
            "errors": ["File does not exist: %s" % vcf_path],
            "warnings": [],
            "details": details,
        }, indent=2)
 
    details["size_bytes"] = os.path.getsize(vcf_path)
    if details["size_bytes"] == 0:
        return json.dumps({
            "status": "INVALID",
            "errors": ["File is empty (0 bytes): %s" % vcf_path],
            "warnings": [],
            "details": details,
        }, indent=2)
 
    # ---- stream the file ------------------------------------------------ #
    chroms = set()
    chr_prefixed = 0
    plain_named = 0
 
    try:
        with _reader(vcf_path) as fh:
            for lineno, raw in enumerate(fh, start=1):
                line = raw.rstrip("\n")
 
                if line.startswith("##"):
                    details["meta_lines"] += 1
                    if line.startswith("##fileformat="):
                        details["fileformat"] = line.split("=", 1)[1].strip()
                    elif line.startswith("##contig"):
                        details["contig_lines"] += 1
                    continue
 
                if line.startswith("#CHROM"):
                    details["has_chrom_header"] = True
                    cols = line.lstrip("#").split("\t")
                    missing = [
                        c for c in REQUIRED_COLUMNS
                        if c not in cols[:len(REQUIRED_COLUMNS)]
                    ]
                    if missing:
                        errors.append(
                            "#CHROM header is missing mandatory columns: %s"
                            % ", ".join(missing)
                        )
                    if len(cols) > 9:
                        details["samples"] = cols[9:]
                        details["sample_count"] = len(cols) - 9
                    elif len(cols) == 9:
                        warnings.append(
                            "FORMAT column present but no sample columns follow."
                        )
                    continue
 
                if not line.strip():
                    continue
 
                if not details["has_chrom_header"]:
                    errors.append(
                        "Data record found at line %d before any #CHROM header."
                        % lineno
                    )
                    details["has_chrom_header"] = True   # report once only
 
                f = line.split("\t")
                bad = None
                if len(f) < 8:
                    bad = "only %d fields, expected at least 8" % len(f)
                elif not f[1].isdigit():
                    bad = "POS is not an integer: %r" % f[1]
                elif not f[3] or not set(f[3].upper()) <= VALID_BASES:
                    bad = "REF is empty or has non-nucleotide characters: %r" % f[3]
                elif not f[4]:
                    bad = "ALT is empty"
 
                if bad:
                    details["malformed_lines"] += 1
                    if len(details["malformed_examples"]) < max_malformed_examples:
                        details["malformed_examples"].append(
                            "line %d: %s" % (lineno, bad)
                        )
                    continue
 
                details["record_count"] += 1
                chrom = f[0]
                chroms.add(chrom)
                if chrom.lower().startswith("chr"):
                    chr_prefixed += 1
                else:
                    plain_named += 1
 
    except (gzip.BadGzipFile, OSError) as exc:
        return json.dumps({
            "status": "INVALID",
            "errors": [
                "File could not be read: %s: %s" % (type(exc).__name__, exc)
            ],
            "warnings": warnings,
            "details": details,
        }, indent=2)
    except Exception as exc:
        return json.dumps({
            "status": "INVALID",
            "errors": [
                "Unexpected error while reading: %s: %s"
                % (type(exc).__name__, exc)
            ],
            "warnings": warnings,
            "details": details,
        }, indent=2)
 
    details["distinct_chromosomes"] = len(chroms)
 
    # ---- structural verdicts -------------------------------------------- #
    if not details["fileformat"]:
        warnings.append(
            "No ##fileformat header found. The file may not be a valid VCF."
        )
    elif not details["fileformat"].upper().startswith("VCFV"):
        warnings.append(
            "Unrecognised ##fileformat value: %r" % details["fileformat"]
        )
 
    if not details["has_chrom_header"]:
        errors.append("No #CHROM header line found. This is not a valid VCF.")
 
    if details["record_count"] == 0:
        errors.append("No usable variant records found.")
 
    if details["malformed_lines"]:
        share = details["malformed_lines"] / float(
            details["malformed_lines"] + details["record_count"]
        )
        msg = "%d malformed data lines were skipped." % details["malformed_lines"]
        if share > 0.10:
            errors.append(msg + " That is %.1f%% of all data lines." % (share * 100))
        else:
            warnings.append(msg)
 
    if chr_prefixed and plain_named:
        details["chrom_naming"] = "mixed"
        warnings.append(
            "Chromosome names mix 'chr'-prefixed and plain styles (%d vs %d). "
            "This often indicates a merged or partially lifted-over file."
            % (chr_prefixed, plain_named)
        )
    elif chr_prefixed:
        details["chrom_naming"] = "chr-prefixed"
    elif plain_named:
        details["chrom_naming"] = "plain"
 
    if details["sample_count"] == 0 and details["record_count"]:
        warnings.append(
            "Sites-only VCF: no sample columns, so genotype-level checks are "
            "not possible."
        )
 
    status = "INVALID" if errors else (
        "VALID_WITH_WARNINGS" if warnings else "VALID"
    )
 
    return json.dumps({
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "details": details,
    }, indent=2, default=str)