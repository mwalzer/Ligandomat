__author__ = 'Backert'
"""File contains queries strings:

 - search_by_sequence_first
 - search_all
 - search_by_runname
 - search_by_organ
 - search_by_tissue
"""

query_source_info = """
SELECT
	source.name,
	source.organ,
	source.dignity,
	source.tissue,
	GROUP_CONCAT(DISTINCT hlaallele.gene_group
        SEPARATOR ', ') as 'hlatype'
FROM
		source
		INNER JOIN source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
WHERE source.name LIKE "%s"
GROUP BY source.name
"""

query_run_name_info_peptides = """
SELECT
	filename,
	ms_run.date,
	source.name,
	source.organ,
	source.dignity,
	source.tissue,
	person.first_name,
	person.last_name,
	mhcpraep.sample_mass,
	mhcpraep.antibody_set,
	mhcpraep.antibody_mass,
	GROUP_CONCAT(DISTINCT hlaallele.gene_group
        SEPARATOR ', ') as 'hlatype',
	Count(DISTINCT sequence) as number_of_peptides
FROM
	ms_run
		INNER JOIN source ON source_id = ms_run.source_source_id
		INNER JOIN source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
		INNER JOIN mhcpraep ON mhcpraep_id = ms_run.mhcpraep_mhcpraep_id
		INNER JOIN person ON person_id = ms_run.person_person_id
		INNER JOIN spectrum_hit ON ms_run_ms_run_id = ms_run_id AND ionscore >20 AND e_value<1 AND q_value <1
		INNER JOIN peptide ON peptide_id = peptide_peptide_id
WHERE filename LIKE '%s'
GROUP BY filename
"""

query_run_name_info = """
SELECT
	filename,
	ms_run.date,
	source.name,
	source.organ,
	source.dignity,
	source.tissue,
	person.first_name,
	person.last_name,
	mhcpraep.sample_mass,
	mhcpraep.antibody_set,
	mhcpraep.antibody_mass,
	GROUP_CONCAT(DISTINCT hlaallele.gene_group
        SEPARATOR ', ') as 'hlatype'
FROM
	ms_run
		INNER JOIN source ON source_id = ms_run.source_source_id
		INNER JOIN source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
		INNER JOIN mhcpraep ON mhcpraep_id = ms_run.mhcpraep_mhcpraep_id
		INNER JOIN person ON person_id = ms_run.person_person_id
WHERE filename LIKE "%s"
GROUP BY filename
"""

search_query_new = """
SELECT
        sequence,
    GROUP_CONCAT(DISTINCT source.name SEPARATOR ', ') AS sourcename,
    GROUP_CONCAT(DISTINCT gene_group
        SEPARATOR ', ') as 'hlatype',
    ROUND(MIN(RT), 2) as minRT,
    ROUND(MAX(RT), 2) as maxRT,
    ROUND(MIN(MZ), 2) as minMZ,
    ROUND(MAX(MZ), 2) as maxMZ,
    MIN(ionscore) as minScore,
    MAX(ionscore) as maxScore,
    MIN(e_value) as minE,
    MAX(e_value) as maxE,
    GROUP_CONCAT(DISTINCT filename
        SEPARATOR ', ') as 'runnames',
    antibody_set,
    GROUP_CONCAT(DISTINCT organ SEPARATOR ', ') as organ,
    GROUP_CONCAT(DISTINCT tissue SEPARATOR ', ') as tissue,
    GROUP_CONCAT(DISTINCT dignity SEPARATOR ', ') as dignity,
    peptide_id,
    peptide_peptide_id,
    ms_run_id,
    ms_run_ms_run_id,
    source_id,
    ms_run.source_source_id,
    mhcpraep_id,
    mhcpraep_mhcpraep_id,
    person_id,
    ms_run.person_person_id,
    source_hlatyping.source_source_id,
	hlaallele_id,
	source_hlatyping.hlaallele_hlaallele_id
FROM
    peptide
        INNER JOIN	spectrum_hit ON peptide_id = peptide_peptide_id
        INNER JOIN	ms_run ON ms_run_id = ms_run_ms_run_id
        INNER JOIN	source ON source_id = source_source_id
        INNER JOIN	mhcpraep ON mhcpraep_id = mhcpraep_mhcpraep_id
        INNER JOIN	person ON person_id = ms_run.person_person_id
		INNER JOIN	source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN	hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id


"""



search_by_sequence_first = """
    SELECT
    sequence,
    sourcename,
    GROUP_CONCAT(DISTINCT gene_group
        SEPARATOR ', ') as 'hlatype',
    ROUND(MIN(RT), 2) as minRT,
    ROUND(MAX(RT), 2) as maxRT,
    ROUND(MIN(MZ), 2) as minMZ,
    ROUND(MAX(MZ), 2) as maxMZ,
    MIN(ionscore) as minScore,
    MAX(ionscore) as maxScore,
    MIN(e_value) as minE,
    MAX(e_value) as maxE,
    GROUP_CONCAT(DISTINCT runname
        SEPARATOR ', ') as 'runnames',
    antibody_set,
    organ,
    tissue,
    dignity
FROM
    (SELECT
        *
    FROM
        ((SELECT
        sequence,
		peptide_id
    FROM
        peptide
	%s )pep_select
    INNER JOIN (SELECT
        ms_run_ms_run_id as peptidems_id,
            sequence,
            RT,
            MZ,
            ionscore,
            e_value,
			peptide_peptide_id
    FROM
        spectrum_hit
	%s ) spectrum_hits  ON pep_select.peptide_id = spectrum_hits.peptide_peptide_id )  peptide
    INNER JOIN ((SELECT
        ms_run_id,
            source_source_id as mssource_id,
            filename as runname,
            antibody_set
    FROM
        ms_run
	%s ) ms_runs
    INNER JOIN mhcpraep ON mhcpraep_mhcpraep_id = mhcpraep_id) ms ON ms_run_id = peptidems_id) peprun
        INNER JOIN
    ((SELECT
        source_id,
            name as sourcename,
            organ,
            tissue,
            dignity
    FROM
        source
	%s )sources
    INNER JOIN (SELECT
        source_source_id as typing_source_id

    FROM
        source_hlatyping
    INNER JOIN hlaallele ON hlaallele_hlaallele_id = hlaallele_id) typing ON source_id = typing_source_id) source ON sources.source_id = mssource_id
GROUP BY sourcename
"""

search_all="SELECT DISTINCT sequence FROM spectrum_hit INNER JOIN peptide ON peptide_id = peptide_peptide_id"


search_by_runname = """
SELECT
    sequence,
    RT,
    MZ,
    ionscore,
    e_value,
    antibody_set,
    sourcename,
    organ,
    tissue,
    dignity,
    gene_group
FROM
    (SELECT
        *
    FROM
        (SELECT
        ms_run_ms_run_id as peptidems_id,
            sequence,
            RT,
            MZ,
            ionscore,
            e_value
    FROM
        spectrum_hit
    INNER JOIN peptide ON peptide_id = peptide_peptide_id
    WHERE
        ionscore > 19 AND e_value < 1) peptide
    INNER JOIN (SELECT
        ms_run_id,
            source_source_id as mssource_id,
            filename as runname,
            antibody_set,
            sample_mass,
            sample_volume
    FROM
        ms_run
    INNER JOIN mhcpraep ON mhcpraep_mhcpraep_id = mhcpraep_id
    WHERE
        filename like '%s') ms ON ms_run_id = peptidems_id) peprun
        INNER JOIN
    (SELECT
        source_id,
            name as sourcename,
            organ,
            tissue,
            dignity,
            typing_source_id,
            gene_group,
            specific_protein,
            dna_coding,
            dna_noncoding,
            expression_suffix
    FROM
        source
    INNER JOIN (SELECT
        source_source_id as typing_source_id,
            gene_group,
            specific_protein,
            dna_coding,
            dna_noncoding,
            expression_suffix
    FROM
        source_hlatyping
    INNER JOIN hlaallele ON hlaallele_hlaallele_id = hlaallele_id) typing ON source_id = typing_source_id) source ON source_id = mssource_id
ORDER BY %s ASC LIMIT 0, 10000
"""



search_by_organ= """
SELECT
    sequence,
    sourcename,
    GROUP_CONCAT(DISTINCT gene_group
        SEPARATOR ', ') as 'hlatype',
    ROUND(MIN(RT), 2) as minRT,
    ROUND(MAX(RT), 2) as maxRT,
    ROUND(MIN(MZ), 2) as minMZ,
    ROUND(MAX(MZ), 2) as maxMZ,
    MIN(ionscore) as minScore,
    MAX(ionscore) as maxScore,
    MIN(e_value) as minE,
    MAX(e_value) as maxE,
    GROUP_CONCAT(DISTINCT filename
        SEPARATOR ', ') as 'runnames',
    antibody_set,
    organ,
    tissue,
    dignity
from
    ((((((SElECT
        source_id, name as sourcename, organ, tissue, dignity
    from
        source
    WHERE
        organ = '%s') organs
    INNER JOIN (SELECT
        source_source_id, hlaallele_hlaallele_id
    FROM
        source_hlatyping) source_hlatypings ON source_hlatypings.source_source_id = organs.source_id)
    INNER JOIN (Select
        hlaallele_id, gene_group
    from
        hlaallele) hlaallele_select ON source_hlatypings.hlaallele_hlaallele_id = hlaallele_select.hlaallele_id)
    INNER JOIN (SELECT
        ms_run_id, source_source_id, filename, mhcpraep_mhcpraep_id
    FROM
        ms_run) ms_runs ON ms_runs.source_source_id = source_id)
    INNER JOIN (SELECT
        mhcpraep_id, antibody_set
    FROM
        mhcpraep) mhcpraeps ON mhcpraep_mhcpraep_id = mhcpraeps.mhcpraep_id)
    INNER JOIN (SELECT
        RT,
            MZ,
            ionscore,
            e_value,
            ms_run_ms_run_id,
            peptide_peptide_id
    FROM
        spectrum_hit
    WHERE
        ionscore > 19 AND e_value < 1) spectrum_hits ON spectrum_hits.ms_run_ms_run_id = ms_run_id)
        INNER JOIN
        ( SELECT
		peptide_id,
		sequence
	FROM peptide) peptides ON spectrum_hits.peptide_peptide_id = peptides.peptide_id
GROUP BY sequence
ORDER BY %s ASC
LIMIT 0 , 10000

"""

search_by_tissue = """	SELECT
    sequence,
    sourcename,
    GROUP_CONCAT(DISTINCT gene_group
        SEPARATOR ', ') as 'hlatype',
    ROUND(MIN(RT), 2) as minRT,
    ROUND(MAX(RT), 2) as maxRT,
    ROUND(MIN(MZ), 2) as minMZ,
    ROUND(MAX(MZ), 2) as maxMZ,
    MIN(ionscore) as minScore,
    MAX(ionscore) as maxScore,
    MIN(e_value) as minE,
    MAX(e_value) as maxE,
    GROUP_CONCAT(DISTINCT filename
        SEPARATOR ', ') as 'runnames',
    antibody_set,
    organ,
    tissue,
    dignity
from
    ((((((SElECT
		source_id,
		name as sourcename,
		organ,
		tissue,
		dignity
    from
        source
    WHERE
        tissue = '%s') tissues
        INNER JOIN
    source_hlatyping ON source_hlatyping.source_source_id =tissues.source_id
        )INNER JOIN
	(Select
		hlaallele_id,
		gene_group
	from hlaallele) hlaallele_select ON source_hlatyping.hlaallele_hlaallele_id = hlaallele_select.hlaallele_id
		)INNER JOIN
		(SELECT
        ms_run_id,
		source_source_id,
        filename,
		mhcpraep_mhcpraep_id
    FROM
		ms_run) ms_runs ON ms_runs.source_source_id = source_id
		)INNER JOIN
	(SELECT
		mhcpraep_id,
		antibody_set,
		sample_mass,
		sample_volume
	FROM mhcpraep
	)mhcpraeps ON mhcpraep_mhcpraep_id = mhcpraeps.mhcpraep_id
		)INNER JOIN

	spectrum_hit ON ms_run_ms_run_id = ms_run_id
		) INNER JOIN ( SELECT
		peptide_id,
		sequence
	FROM peptide) peptides ON ON peptide_peptide_id = peptides.peptide_id  WHERE ionscore >19 AND e_value <1

GROUP BY sequence ORDER BY %s  ASC LIMIT 0, 10000



"""