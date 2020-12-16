import sys
import os
import re


def get_sample(path):
    filename, ext = os.path.splitext(os.path.basename(path))
    if filename.find('.recode') != -1:
        filename = filename[:filename.find('.recode')]
    return filename


def main(vcf, output):
    fo = open(output, 'w')
    with open(vcf, 'r') as file:
        for line in file:
            line = line.rstrip()
            fields = line.split('\t')

            if re.search('^#', line):
                print(line, file=fo)

            else:
                fields[8] = 'GT:' + fields[8]
                fields[9] = '0/1:' + fields[9]
                print(*fields, file=fo, sep="\t")

    fo.close()


if __name__ == "__main__":
    try:
        vcf = sys.argv[1]
        sample = get_sample(vcf)
        output = os.path.join(os.path.dirname(vcf), sample + ".reformatted.vcf")


    except:
        print("Usage reformat-for_annovar.py sample.recode.vcf")
        sys.exit(1)

    main(vcf, output)