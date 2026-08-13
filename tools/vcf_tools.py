from pathlib import Path
import subprocess

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

    file_name = str(path).lower()

    if not (
        file_name.endswith(".vcf")
        or file_name.endswith(".vcf.gz")
    ):
        return (
            "VCF VALIDATION RESULT\n"
            "Status: INVALID\n"
            "Reason: File must have a .vcf or .vcf.gz extension."
        )

    try:
        reader = vcfpy.Reader.from_path(str(path))

        variant_count = 0
        examples = []

        for record in reader:
            variant_count += 1

            if len(examples) < 5:
                examples.append(
                    {
                        "chromosome": record.CHROM,
                        "position": record.POS,
                        "reference": record.REF,
                        "alternative": [
                            str(alt.value) for alt in record.ALT
                        ],
                        "filter": record.FILTER,
                    }
                )

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


@tool("bcftools_stats")
def bcftools_stats(file_path: str) -> str:
    """
    Run bcftools stats on a VCF and return key QC summary statistics.
    """

    path = Path(file_path)

    if not path.exists():
        return (
            "BCFTOOLS STATS RESULT\n"
            "Status: FAILED\n"
            f"Reason: File does not exist: {file_path}"
        )

    try:
        result = subprocess.run(
            ["bcftools", "stats", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return (
                "BCFTOOLS STATS RESULT\n"
                "Status: FAILED\n"
                f"Error: {result.stderr.strip()}"
            )

        summary_lines = []

        for line in result.stdout.splitlines():
            if line.startswith("SN"):
                fields = line.split("\t")

                if len(fields) >= 4:
                    metric = fields[2].rstrip(":")
                    value = fields[3]
                    summary_lines.append(
                        f"{metric}: {value}"
                    )

        if not summary_lines:
            return (
                "BCFTOOLS STATS RESULT\n"
                "Status: SUCCESS\n"
                "No summary-number records were returned."
            )

        return (
            "BCFTOOLS STATS RESULT\n"
            "Status: SUCCESS\n"
            + "\n".join(summary_lines)
        )

    except FileNotFoundError:
        return (
            "BCFTOOLS STATS RESULT\n"
            "Status: FAILED\n"
            "Reason: bcftools is not installed or is not available in PATH."
        )

    except Exception as e:
        return (
            "BCFTOOLS STATS RESULT\n"
            "Status: FAILED\n"
            f"Error: {type(e).__name__}: {e}"
        )


@tool("filter_vcf")
def filter_vcf(file_path: str, output_path: str) -> str:
    """
    Retain variants with FILTER=PASS and write them to a separate VCF.

    The original VCF is preserved.
    """

    input_path = Path(file_path)
    output = Path(output_path)

    if not input_path.exists():
        return (
            "VCF FILTERING RESULT\n"
            "Status: FAILED\n"
            f"Reason: File does not exist: {file_path}"
        )

    try:
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        before = subprocess.run(
            [
                "bcftools",
                "view",
                "-H",
                str(input_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if before.returncode != 0:
            return (
                "VCF FILTERING RESULT\n"
                "Status: FAILED\n"
                f"Reason: Unable to read input VCF.\n"
                f"{before.stderr.strip()}"
            )

        before_count = len(
            [
                line
                for line in before.stdout.splitlines()
                if line.strip()
            ]
        )

        result = subprocess.run(
            [
                "bcftools",
                "view",
                "-f",
                "PASS",
                "-O",
                "v",
                "-o",
                str(output),
                str(input_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return (
                "VCF FILTERING RESULT\n"
                "Status: FAILED\n"
                f"Reason: Filtering failed.\n"
                f"{result.stderr.strip()}"
            )

        after = subprocess.run(
            [
                "bcftools",
                "view",
                "-H",
                str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if after.returncode != 0:
            return (
                "VCF FILTERING RESULT\n"
                "Status: FAILED\n"
                f"Reason: Unable to inspect filtered VCF.\n"
                f"{after.stderr.strip()}"
            )

        after_count = len(
            [
                line
                for line in after.stdout.splitlines()
                if line.strip()
            ]
        )

        removed_count = before_count - after_count

        return (
            "VCF FILTERING RESULT\n"
            "Status: SUCCESS\n"
            f"Input variants: {before_count}\n"
            f"Retained PASS variants: {after_count}\n"
            f"Removed variants: {removed_count}\n"
            f"Output file: {output}"
        )

    except FileNotFoundError:
        return (
            "VCF FILTERING RESULT\n"
            "Status: FAILED\n"
            "Reason: bcftools is not installed or is not available in PATH."
        )

    except Exception as e:
        return (
            "VCF FILTERING RESULT\n"
            "Status: FAILED\n"
            f"Error: {type(e).__name__}: {e}"
        )


@tool("parse_vcf")
def parse_vcf(file_path: str) -> str:
    """
    Parse a VCF and return basic structured information for each variant.
    """

    path = Path(file_path)

    if not path.exists():
        return (
            "VCF PARSING RESULT\n"
            "Status: FAILED\n"
            f"Reason: File does not exist: {file_path}"
        )

    try:
        reader = vcfpy.Reader.from_path(str(path))

        variants = []

        for record in reader:
            variants.append(
                {
                    "id": record.ID,
                    "chromosome": record.CHROM,
                    "position": record.POS,
                    "reference": record.REF,
                    "alternative": [
                        str(alt.value) for alt in record.ALT
                    ],
                    "quality": record.QUAL,
                    "filter": record.FILTER,
                }
            )

        reader.close()

        return (
            "VCF PARSING RESULT\n"
            "Status: SUCCESS\n"
            f"Parsed variants: {len(variants)}\n"
            f"Variants: {variants}"
        )

    except Exception as e:
        return (
            "VCF PARSING RESULT\n"
            "Status: FAILED\n"
            f"Error: {type(e).__name__}: {e}"
        )