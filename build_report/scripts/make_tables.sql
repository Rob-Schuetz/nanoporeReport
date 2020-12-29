drop view if exists report.nanopore_report;
drop view if exists report.targets_present;
drop table if exists report.unique_vcf_rows;
drop table if exists report.vcf_pass;
drop table if exists report.historical_pass;
drop table if exists report.targets;
drop table if exists report.testy;



create table if not exists report.unique_vcf_rows
(
	sample varchar(50),
	chrom varchar(10),
	pos integer
);

alter table report.unique_vcf_rows owner to postgres;

create table if not exists report.vcf_pass
(
	sample varchar(50),
	chrom varchar(10),
	pos1 integer,
	pos integer,
	ref varchar(50),
	alt varchar(50),
	vaf numeric(50,10),
	depth integer,
	gene_name varchar(100),
	gene_func varchar(100)
);

alter table report.vcf_pass owner to postgres;

create table if not exists report.historical_pass
(
	sample varchar(50),
	chrom varchar(10),
	pos1 integer,
	pos integer,
	ref varchar(50),
	alt varchar(50),
	vaf numeric(50),
	depth integer,
	gene_name varchar(100),
	gene_func varchar(100),
	created_at timestamp default now()
);

alter table report.historical_pass owner to postgres;

create table if not exists report.targets
(
	sample varchar(50),
	chrom varchar(10),
	pos1 integer,
	pos integer,
	target_desc varchar(100)
);

alter table report.targets owner to postgres;

create table if not exists report.testy
(
	vaf real
);

alter table report.testy owner to postgres;



create view report.nanopore_report
as
    with t as (

        select *
        from report.targets
        group by sample, chrom, pos1, pos, target_desc

    ),

    res as (

        select *
        from report.results
        group by sample, chrom, pos1, pos, ref, alt, vaf, depth, gene_name, gene_func

    )

    select *
    from (
            select concat(res.chrom, ':', res.pos1) mutated_pos,
            t.target_desc,
            cast(substring(t.chrom from position('chr' in t.chrom) + char_length('chr')) as int) as chrom_num,
            res.gene_name,
            res.gene_func,
            cast(round(res.vaf,5) as varchar) vaf,
            res.depth,
            case when res.vaf < 0.05 then 'Not present'
                 when res.depth < 100 then 'Not present'
                 when res.vaf is null and res.depth is null then 'Not present'
                 else 'Present'
                 end as call,
            case when res.vaf < 0.05 then 'Low VAF'
                 when res.depth < 100 then 'Low Coverage'
                 else ''
                 end as comments,
            t.sample

            from t
            left join res on concat(res.chrom, res.pos1) = concat(t.chrom, t.pos1)
         ) a
    order by chrom_num, mutated_pos
;

alter table report.nanopore_report owner to postgres;


create view report.targets_present
as
    with t as (

            select *
            from report.targets
            group by sample, chrom, pos1, pos, target_desc

        ),

        uni as (

            select *
            from report.unique_vcf_rows
            group by sample, chrom, pos

        )

        select t.*,
               case when uni.sample is null then 'Not Present' else 'Present' end as present
        from t
        left join uni on uni.chrom = t.chrom and uni.pos between t.pos1 and t.pos
        group by t.sample, t.chrom, t.pos1, t.pos, t.target_desc, uni.sample
        order by t.sample, t.chrom
;

alter table report.targets_present owner to postgres;



create view report.final_results
as
    with pass_results as (
        select target_desc,
            gene_name,
            gene_func,
            vaf,
            depth,
            STRING_AGG(mutated_pos, ', ' order by mutated_pos) mutations
        from report.nanopore_report
        where mutated_pos != ':'
        group by target_desc, gene_name, gene_func, vaf, depth
        )

    select t.sample,
        t.target_desc,
        concat(t.chrom, ':', pos1, '-', pos) target_range,
        pr.mutations,
        pr.gene_name,
        pr.gene_func,
        pr.vaf,
        pr.depth,
        case when mutations is null then 'No mutation detected' else 'Mutated' end as is_mutated



    from report.targets_present t
    left join pass_results pr on t.target_desc = pr.target_desc
    where t.present = 'Present'

alter table report.final_results owner to postgres;
