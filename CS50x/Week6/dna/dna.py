import csv
import sys

def main():

    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    with open(sys.argv[1], "r") as file:
        content = list(csv.DictReader(file))
        nucleotides = list(content[0].keys())
        nucleotides.remove("name")

    with open(sys.argv[2], "r") as file:
        sequence = file.read().strip()

    count = {}
    for nucleotide in nucleotides:
        count[nucleotide] = longest_match(sequence, nucleotide)

    for row in content:
        if all(count[nucleotide] == int(row[nucleotide]) for nucleotide in nucleotides):
            print(row["name"])
            return

    print("No match")

def longest_match(sequence, nucleotide):
    maxCount = 0
    currCount = 0
    i, lenSubStr = 0, len(nucleotide)

    while i <= len(sequence) - lenSubStr  :

        if sequence[i:i + lenSubStr] == nucleotide:
            currCount += 1
            i += lenSubStr
        else:
            maxCount = max(maxCount, currCount)
            currCount = 0
            i += 1

    maxCount = max(maxCount, currCount) # IF LONGEST CONSECUTIVE SUBSTRINGS ENDS AT LAST INDEX OF STRING.
    return maxCount

main()
