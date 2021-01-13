import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..', '..', 'snakemake'))
sys.path.append(os.path.join(os.getcwd(), '..', 'snakemake'))
sys.path.append(os.path.join(os.getcwd(), 'snakemake'))
from genomics import get_config


def main(filepath):
    input_dir = os.path.dirname(filepath)

    sample, file_ext = os.path.splitext(os.path.basename(filepath))
    if sample.find('.annotated') != -1:
        sample = sample[:sample.find('.annotated')]

    anno_input = os.path.join(input_dir, sample + ".annotated.vcf.avinput")
    #anno_vcf = os.path.join(input_dir, sample + ".annotated.vcf." + get_config.main("nanoporeReport", "build") + "_multianno.vcf")
    anno_txt = os.path.join(input_dir, sample + ".annotated.vcf." + get_config.main("nanoporeReport", "build") + "_multianno.txt")
    anno_output_vcf = os.path.join(input_dir, sample + ".annotated.vcf")

    if filepath != anno_output_vcf:
        os.rename(filepath, anno_output_vcf)
    else:
        print("Designated file has already been renamed")

    try:
        os.remove(anno_input)
    except:
        print("No .avinput file to remove")

    try:
        os.remove(anno_txt)
    except:
        print("No multianno.txt file to remove")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage python rename_annovar.py filepath")
        sys.exit(1)

    path = args[0]
    main(path)
