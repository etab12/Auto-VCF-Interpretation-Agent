#test

from crew import crew


if __name__ == "__main__":

    print("=" * 60)
    print("GENOMICS VARIANT ANALYSIS SYSTEM")
    print("=" * 60)

    result = crew.kickoff()

    print("\n")
    print("=" * 60)
    print("FINAL REPORT")
    print("=" * 60)
    print(result)
