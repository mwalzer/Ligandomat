__author__ = 'Backert'
"""File contains queries strings
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
		LigandosphereDB_dev.source
		INNER JOIN LigandosphereDB_dev.source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN LigandosphereDB_dev.hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
WHERE source.name LIKE "%s"
GROUP BY source.name
"""
query_source_info_peptides = """
SELECT
	source.name,
	source.organ,
	source.dignity,
	source.tissue,
	GROUP_CONCAT(DISTINCT hlaallele.gene_group
        SEPARATOR ', ') as 'hlatype',
	Count(DISTINCT sequence) as number_of_peptides
FROM
		LigandosphereDB_dev.source
		INNER JOIN LigandosphereDB_dev.source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN LigandosphereDB_dev.hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
		INNER JOIN LigandosphereDB_dev.ms_run ON ms_run.source_source_id = source.source_id
		INNER JOIN LigandosphereDB_dev.spectrum_hit ON ms_run_ms_run_id = ms_run_id AND ionscore >%s AND e_value<%s AND q_value <%s
		INNER JOIN LigandosphereDB_dev.peptide ON peptide_id = peptide_peptide_id
WHERE source.name LIKE '%s'
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
	LigandosphereDB_dev.ms_run
		INNER JOIN LigandosphereDB_dev.source ON source_id = ms_run.source_source_id
		INNER JOIN LigandosphereDB_dev.source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN LigandosphereDB_dev.hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
		INNER JOIN LigandosphereDB_dev.mhcpraep ON mhcpraep_id = ms_run.mhcpraep_mhcpraep_id
		INNER JOIN LigandosphereDB_dev.person ON person_id = ms_run.person_person_id
		INNER JOIN LigandosphereDB_dev.spectrum_hit ON ms_run_ms_run_id = ms_run_id AND ionscore >%s AND e_value<%s AND q_value <%s
		INNER JOIN LigandosphereDB_dev.peptide ON peptide_id = peptide_peptide_id
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
	LigandosphereDB_dev.ms_run
		INNER JOIN LigandosphereDB_dev.source ON source_id = ms_run.source_source_id
		INNER JOIN LigandosphereDB_dev.source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN LigandosphereDB_dev.hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
		INNER JOIN LigandosphereDB_dev.mhcpraep ON mhcpraep_id = ms_run.mhcpraep_mhcpraep_id
		INNER JOIN LigandosphereDB_dev.person ON person_id = ms_run.person_person_id
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
	source_hlatyping.hlaallele_hlaallele_id,
	GROUP_CONCAT(DISTINCT peptide_mapping.uniprot_accession_pm SEPARATOR ', ') as uniprot_accession
FROM
    LigandosphereDB_dev.peptide
        INNER JOIN	LigandosphereDB_dev.spectrum_hit ON peptide_id = peptide_peptide_id
        INNER JOIN	LigandosphereDB_dev.ms_run ON ms_run_id = ms_run_ms_run_id
        INNER JOIN	LigandosphereDB_dev.source ON source_id = source_source_id
        INNER JOIN	LigandosphereDB_dev.mhcpraep ON mhcpraep_id = mhcpraep_mhcpraep_id
        INNER JOIN	LigandosphereDB_dev.person ON person_id = ms_run.person_person_id
		INNER JOIN	LigandosphereDB_dev.source_hlatyping ON source_hlatyping.source_source_id = source_id
		INNER JOIN	LigandosphereDB_dev.hlaallele ON hlaallele_id = source_hlatyping.hlaallele_hlaallele_id
		INNER JOIN	UniprotMapping.peptide_mapping ON peptide_mapping.ligandosphere_peptide_peptide_id = peptide_id
"""

