from __future__ import print_function
import sys
import os
import re
import pandas as pd
import psycopg2
sys.path.append(os.path.join(os.getcwd(), '..', '..', 'snakemake'))
sys.path.append(os.path.join(os.getcwd(), '..', 'snakemake'))
sys.path.append(os.path.join(os.getcwd(), 'snakemake'))
from genomics import get_config


def get_sample(path):
    filename, ext = os.path.splitext(os.path.basename(path))
    if filename.find(".annotated") != -1:
        filename = filename[:filename.find(".annotated")]
    return filename


def execute_sql(conn, insert_req):
    """ Execute a single INSERT request """
    cursor = conn.cursor()
    try:
        cursor.execute(insert_req)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()


def main(input_file, output):

    # ENSURE DIRECTORY IS PRESENT
    
    if not os.path.exists(os.path.dirname(output)):
        os.mkdir(os.path.dirname(output))

    # READ FILE AND BUILD DATAFRAME

    fo = open(output, 'w')
    sample_name = get_sample(input_file)
    print("sample", "chrom", "pos", file=fo, sep="\t")
    with open(input_file, 'r') as file:
        for line in file:
            line = line.rstrip()
            fields = line.split('\t')

            if not re.search("^#", line):
                chrom = fields[0]
                pos = int(fields[1])

                print(sample_name, chrom, pos, file=fo, sep="\t")

    fo.close()

    df = pd.read_csv(output, sep="\t")
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)


    # ADD INPUT FILES TO DB
    conn_dict = {
        'host': get_config.main("database", "hostname"),
        'port': get_config.main("database", "port"),
        'user': get_config.main("database", "username"),
        'password': get_config.main("database", "password"),
        'database': get_config.main("database", "db")
    }

    # ADD VCF TO RESULTS TABLE

    try:
        conn = psycopg2.connect(**conn_dict)
        delete_command = "DELETE FROM %s where 1=1;"%(get_config.main("database", "unique_vcf_rows"))
        execute_sql(conn, delete_command)

        # Inserting each row
        for i, row in df.iterrows():
            query = "INSERT into %s values ('%s', '%s', %s);"%(get_config.main("database", "unique_vcf_rows"), row['sample'], row['chrom'], row['pos'])
            execute_sql(conn, query)
        conn.close()

    except:
        print('Failed to add vcf data to results table')
        conn.close()



if __name__ == "__main__":
    arguments = sys.argv[1:]
    count = len(arguments)

    if count != 2:
        print("Usage: python store_unique_vcf_lines.py input_vcf output")
        sys.exit(1)
    elif count == 2:
        input_vcf = arguments[0]
        output = arguments[1]

    main(input_vcf, output)