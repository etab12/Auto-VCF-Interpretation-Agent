from pathlib import Path

from crewai.tools import tool


@tool("validate_vcf")
def validate_vcf(file_path: str) -> str:
    """
    Validate a VCF file.

    Checks whether the file exists, can be opened as a VCF,
    and contains genomic variant records.
    """

    path = Path(file_path)

    # Check file exists
    if not path.exists():
        return (
            "VCF VALIDATION RESULT\n"
            "Status: INVALID\n"
            f"Reason: File does not exist: {file_path}"
        )

    # Check extension
    if path.suffix.lower() != ".vcf":
        return (
            "VCF VALIDATION RESULT\n"
            "Status: INVALID\n"
            "Reason: File must have a .vcf extension."
        )

    try:
        from cyvcf2 import VCF

        vcf = VCF(str(path))

        variant_count = 0
        first_variants = []

        for variant in vcf:
            variant_count += 1

            if len(first_variants) < 5:
                first_variants.append(
                    {
                        "chromosome": variant.CHROM,
                        "position": variant.POS,
                        "reference": variant.REF,
                        "alternative": list(variant.ALT),
                    }
                )

        vcf.close()

        if variant_count == 0:
            return (
                "VCF VALIDATION RESULT\n"
                "Status: INVALID\n"
                "Reason: The VCF contains no variant records."
            )

        return (
            "VCF VALIDATION RESULT\n"
            "Status: VALID\n"
            f"File: {path.name}\n"
            f"Variant count: {variant_count}\n"
            f"Example variants: {first_variants}"
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
    Read a VCF file and extract basic information about its variants.
    """

    path = Path(file_path)

    if not path.exists():
        return f"ERROR: File does not exist: {file_path}"

    try:
        from cyvcf2 import VCF

        vcf = VCF(str(path))

        variants = []

        for variant in vcf:
            variants.append(
                {
                    "chromosome": variant.CHROM,
                    "position": variant.POS,
                    "reference": variant.REF,
                    "alternative": list(variant.ALT),
                }
            )

        vcf.close()

        return (
            f"Parsed {len(variants)} variants.\n\n"
            f"Variants:\n{variants}"
        )

    except Exception as e:
        return (
            f"ERROR while parsing VCF: "
            f"{type(e).__name__}: {e}"
        )