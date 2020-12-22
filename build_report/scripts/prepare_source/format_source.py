<<<<<<< HEAD
#!/usr/bin/env python3
# import commands
from __future__ import print_function
import sys
import os
import re
import pandas as pd
import psycopg2
sys.path.append(os.path.join(os.getcwd(), '..', '..', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), '..', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
from genomics import get_config


def get_sample(path):
    filename, ext = os.path.splitext(os.path.basename(path))
    if filename.find(".annotated") != -1:
        filename = filename[:filename.find(".annotated")]
    return filename


def get_sample_column(sample_type, line):
    line = line.lstrip('#')
    headers = line.split('\t')
    for i, h in enumerate(headers):
        if sample_type == "tumor" and h.find('_t') != -1:
            column_pos = i
        if sample_type == "normal" and h.find('_g') != -1:
            column_pos = i
    try:
        return column_pos
    except:
        return len(headers) - 1


def get_vinfo(info, fields, tumor_column):
    numerical_info = ['AF']
    keys = fields[8]
    keys = keys.rstrip()
    keys = keys.split(':')
    for i, k in enumerate(keys):
        if k == info:
            info_pos = i

    if 'info_pos' not in locals():
        print('No ' + info + ' in FORMAT column of vcf')
        sys.exit(1)

    try:
        values = fields[tumor_column]
        values = values.rstrip()
        values = values.split(':')
        if info in numerical_info:
            return float(values[info_pos])
        return values[info_pos]
    except:
        return '.'

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


def main(vcf_file, target_file, output):

    # ENSURE DIRECTORY IS PRESENT
    
    if not os.path.exists(os.path.dirname(output)):
        os.mkdir(os.path.dirname(output))

    # WRITE FILE

    fo = open(output, 'w')
    sample_name = get_sample(vcf_file)
    print("sample", "chrom", "pos-1", "pos", "ref", "alt", "VAF", "depth", "gene", "gene_func", file=fo, sep="\t")
    with open(vcf_file, 'r') as file:
        for line in file:
            line = line.rstrip()
            fields = line.split('\t')

            if not re.search("^#", line):
                chrom = fields[0]
                pos = int(fields[1])
                ref = fields[3]
                alt = fields[4]
                vaf = get_vinfo('AF', fields, 9)
                depth = get_vinfo('DP', fields, 9)
                info = fields[7].split(';')
                for i in info:
                    if i.find("Gene.refGene=") != -1:
                        gene = i[i.find("Gene.refGene=") + len("Gene.refGene="):]
                    if i.find("Func.refGene=") != -1:
                        gene_func = i[i.find("Func.refGene=") + len("Func.refGene="):]

                print(vaf)
                print(sample_name, chrom, pos - 1, pos, ref, alt, vaf, depth, gene, gene_func, file=fo, sep="\t")

    fo.close()

    vcf_df = pd.read_csv(output, sep="\t")


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
        delete_command = "DELETE FROM %s where 1=1;"%(get_config.main("database", "vcf_table"))
        execute_sql(conn, delete_command)

        # Inserting each row
        for i, row in vcf_df.iterrows():
            print(row['VAF'])
            query = "INSERT into %s values ('%s', '%s', %s, %s, '%s', '%s', %s, %s, '%s', '%s');"%(get_config.main("database", "vcf_table"), row['sample'], row['chrom'], row['pos-1'], row['pos'], row['ref'], row['alt'], row['VAF'], row['depth'], row['gene'], row['gene_func'])
            print(query)
            execute_sql(conn, query)
        conn.close()

    except:
        print('Failed to add vcf data to results table')
        conn.close()
    

    # ADD VCF TO ALL PASS TABLE

    try:

        conn = psycopg2.connect(**conn_dict)

        # Inserting each row
        for i, row in vcf_df.iterrows():
            query = "INSERT into %s values ('%s', '%s', %s, %s, '%s', '%s', %s, %s, '%s', '%s');"%(get_config.main("database", "all_pass_table"), row['sample'], row['chrom'], row['pos-1'], row['pos'], row['ref'], row['alt'], row['VAF'], row['depth'], row['gene'], row['gene_func'])
            execute_sql(conn, query)
        conn.close()

    except:
        print('Failed to add vcf data to all_pass table')
        conn.close()


    # ADD TARGETS TO TARGETS TABLE

    target_df = pd.read_csv(target_file, sep="\t", header=None)

    try:

        conn = psycopg2.connect(**conn_dict)
        delete_command = "DELETE FROM %s where 1=1;"%(get_config.main("database", "target_table"))
        execute_sql(conn, delete_command)

        # Inserting each row
        for i, row in target_df.iterrows():
            query = "INSERT into %s values ('%s', '%s', %s, %s, '%s');"%(get_config.main("database", "target_table"), sample_name, row[0], row[1], row[2], row[3])
            execute_sql(conn, query)
        conn.close()
        
    except:
        print('Failed to add target data to targets table')
        conn.close()

    # EXPORT FILE
    vcf_df.to_csv(output, index=False)
    


if __name__ == "__main__":
    arguments = sys.argv[1:]
    count = len(arguments)

    if count != 3:
        print("Usage: python format_source.py input_vcf input_targets output_file")
        sys.exit(1)
    elif count == 3:
        input_vcf = arguments[0]
        target_file = arguments[1]
        output_file = arguments[2]

    main(input_vcf, target_file, output_file)
=======
#!/usr/bin/env python3
# import commands
from __future__ import print_function
import sys
import os
import re
import pandas as pd
import psycopg2
sys.path.append(os.path.join(os.getcwd(), '..', '..', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), '..', 'scripts'))
sys.path.append(os.path.join(os.getcwd(), 'scripts'))
from genomics import get_config


def get_sample(path):
    filename, ext = os.path.splitext(os.path.basename(path))
    if filename.find(".annotated") != -1:
        filename = filename[:filename.find(".annotated")]
    return filename


def get_sample_column(sample_type, line):
    line = line.lstrip('#')
    headers = line.split('\t')
    for i, h in enumerate(headers):
        if sample_type == "tumor" and h.find('_t') != -1:
            column_pos = i
        if sample_type == "normal" and h.find('_g') != -1:
            column_pos = i
    try:
        return column_pos
    except:
        return len(headers) - 1


def get_vinfo(info, fields, tumor_column):
    numerical_info = ['AF']
    keys = fields[8]
    keys = keys.rstrip()
    keys = keys.split(':')
    for i, k in enumerate(keys):
        if k == info:
            info_pos = i

    if 'info_pos' not in locals():
        print('No ' + info + ' in FORMAT column of vcf')
        sys.exit(1)

    try:
        values = fields[tumor_column]
        values = values.rstrip()
        values = values.split(':')
        if info in numerical_info:
            return float(values[info_pos])
        return values[info_pos]
    except:
        return '.'

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


def main(vcf_file, target_file, output):

    # ENSURE DIRECTORY IS PRESENT
    
    if not os.path.exists(os.path.dirname(output)):
        os.mkdir(os.path.dirname(output))

    # WRITE FILE

    fo = open(output, 'w')
    sample_name = get_sample(vcf_file)
    print("sample", "chrom", "pos-1", "pos", "ref", "alt", "VAF", "depth", "gene", "gene_func", file=fo, sep="\t")
    with open(vcf_file, 'r') as file:
        for line in file:
            line = line.rstrip()
            fields = line.split('\t')

            if not re.search("^#", line):
                chrom = fields[0]
                pos = int(fields[1])
                ref = fields[3]
                alt = fields[4]
                vaf = get_vinfo('AF', fields, 9)
                depth = get_vinfo('DP', fields, 9)
                info = fields[7].split(';')
                for i in info:
                    if i.find("Gene.refGene=") != -1:
                        gene = i[i.find("Gene.refGene=") + len("Gene.refGene="):]
                    if i.find("Func.refGene=") != -1:
                        gene_func = i[i.find("Func.refGene=") + len("Func.refGene="):]

                print(sample_name, chrom, pos - 1, pos, ref, alt, vaf, depth, gene, gene_func, file=fo, sep="\t")

    fo.close()

    vcf_df = pd.read_csv(output, sep="\t")


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
        delete_command = "DELETE FROM %s where 1=1;"%(get_config.main("database", "vcf_table"))
        execute_sql(conn, delete_command)

        # Inserting each row
        for i, row in vcf_df.iterrows():
            query = "INSERT into %s values ('%s', '%s', %s, %s, '%s', '%s', %s, %s, '%s', '%s');"%(get_config.main("database", "vcf_table"), row['sample'], row['chrom'], row['pos-1'], row['pos'], row['ref'], row['alt'], row['VAF'], row['depth'], row['gene'], row['gene_func'])
            execute_sql(conn, query)
        conn.close()

    except:
        print('Failed to add vcf data to results table')
        conn.close()
    

    # ADD VCF TO ALL PASS TABLE

    try:

        conn = psycopg2.connect(**conn_dict)

        # Inserting each row
        for i, row in vcf_df.iterrows():
            query = "INSERT into %s values ('%s', '%s', %s, %s, '%s', '%s', %s, %s, '%s', '%s');"%(get_config.main("database", "all_pass_table"), row['sample'], row['chrom'], row['pos-1'], row['pos'], row['ref'], row['alt'], row['VAF'], row['depth'], row['gene'], row['gene_func'])
            execute_sql(conn, query)
        conn.close()

    except:
        print('Failed to add vcf data to all_pass table')
        conn.close()


    # ADD TARGETS TO TARGETS TABLE

    target_df = pd.read_csv(target_file, sep="\t", header=None)

    try:

        conn = psycopg2.connect(**conn_dict)
        delete_command = "DELETE FROM %s where 1=1;"%(get_config.main("database", "target_table"))
        execute_sql(conn, delete_command)

        # Inserting each row
        for i, row in target_df.iterrows():
            query = "INSERT into %s values ('%s', '%s', %s, %s, '%s');"%(get_config.main("database", "target_table"), sample_name, row[0], row[1], row[2], row[3])
            execute_sql(conn, query)
        conn.close()
        
    except:
        print('Failed to add target data to targets table')
        conn.close()

    # EXPORT FILE
    vcf_df.to_csv(output, index=False)
    


if __name__ == "__main__":
    arguments = sys.argv[1:]
    count = len(arguments)

    if count != 3:
        print("Usage: python format_source.py input_vcf input_targets output_file")
        sys.exit(1)
    elif count == 3:
        input_vcf = arguments[0]
        target_file = arguments[1]
        output_file = arguments[2]

    main(input_vcf, target_file, output_file)
>>>>>>> 19bcf862de4ddd1af8d7d65f3f744fbf137dfe04
