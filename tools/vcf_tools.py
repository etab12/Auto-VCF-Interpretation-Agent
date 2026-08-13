from pathlib import Path

import vcfpy
from crewai.tools import tool


@tool("validate_vcf")
def validate_vcf(file_path: str) -> str:
    """
    Validate a VCF file and check whether it contains usable variant data.
    """

    path = Path(file_path)

    if not path.exists():
        return (
            "VCF VALIDATION RESULT\n"
            "Status: INVALID\n"
            f"Reason: File does not exist: {file_path}"
        )

    if path.suffix.lower() != ".vcf":
        return (
            "VCF VALIDATION RESULT\n"
            "Status: INVALID\n"
            "Reason: File must have a .vcf extension."
        )

    try:
        reader = vcfpy.Reader.from_path(str(path))

        variant_count = 0
        examples = []

        for record in reader:
            variant_count += 1

            if len(examples) < 5:
                examples.append({
                    "chromosome": record.CHROM,
                    "position": record.POS,
                    "reference": record.REF,
                    "alternative": record.ALT,
                })

        reader.close()

        if variant_count == 0:
            return (
                "VCF VALIDATION RESULT\n"
                "Status: INVALID\n"
                "Reason: No variant records were found."
            )

        return (
            "VCF VALIDATION RESULT\n"
            "Status: VALID\n"
            f"File: {path.name}\n"
            f"Variant count: {variant_count}\n"
            f"Example variants: {examples}"
        )

    except Exception as e:
        return (
            "VCF VALIDATION RESULT\n"
            "Status: INVALID\n"
            f"Error: {type(e).__name__}: {e}"
        )


@tool("parse_vcf")
def parse_vcf(file_path: str) -> str:
    """
    Parse a VCF file and extract basic variant information.
    """

    path = Path(file_path)

    if not path.exists():
        return f"ERROR: File does not exist: {file_path}"

    try:
        reader = vcfpy.Reader.from_path(str(path))

        variants = []

        for record in reader:
            variants.append({
                "chromosome": record.CHROM,
                "position": record.POS,
                "reference": record.REF,
                "alternative": record.ALT,
            })

        reader.close()

        return (
            f"Parsed {len(variants)} variants.\n\n"
            f"Variants:\n{variants}"
        )

    except Exception as e:
        return (
            f"ERROR while parsing VCF: "
            f"{type(e).__name__}: {e}"
        )