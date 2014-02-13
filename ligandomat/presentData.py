from DBtransfer import *


def smallPeptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, Mass_specData, Person, peptides) :

	table = []
	for pep in peptides :
		d = dict()
		d['sequence'] = pep.sequence
		d['length'] = len(pep.sequence)
		table.append(d)
		
	d = dict()
	d['cols'] = ['sequence', 'length']
	d['num_pep'] = len(peptides)
	table.append(d)
	return table
	
		
def peptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, Mass_specData, Person, peptides) :
	
	table = []
	for pep in peptides :
		hits = getAllHitsOfPeptide(DBSession, Peptide, Hit, pep)
		ms_stack = []
		for hit in hits :
			if not hit.ms_run_ms_run_id in ms_stack :
				ms_stack.append(hit.ms_run_ms_run_id)
				ms_run = DBSession.query(Mass_specData).get(hit.ms_run_ms_run_id)
				source = DBSession.query(SourceData).get(ms_run.source_source_id)
				typings = getTypingsBySourceId(DBSession, SourceHLA, source.source_id)
				types = []
				for i in range(0, len(typings)) :
					type = ''
					type += DBSession.query(HLAAllele).get(typings[i].hlaallele_hlaallele_id).gene_group
					if not typings[i].specific_protein is None : #XXX to test
						type += ':'
						type += typings[i].specific_protein
						if not typings[i].dna_coding is None :
							type += ':'
							type += typings[i].dna_coding
							if not typings[i].dna_noncoding is None :
								type += ':'
								type += typings[i].dna_noncoding
								if not typings[i].expession_suffix is None :
									type += typings[i].expession_suffix
					types.append(type)
				prep = DBSession.query(PrepData).get(ms_run.mhcpraep_mhcpraep_id)
				d = dict()
				d['sequence'] = pep.sequence
				d['e_value'] = hit.e_value
				d['person_run'] = getPersonById_Name(DBSession, Person, ms_run.person_person_id)
				d['source_name'] = source.name
				d['source_dignity'] = source.dignity
				d['typings'] = types
				table.append(d)
	d = dict()
	d['cols'] = ['sequence', 'e_value', 'person_run', 'source_name', 'source_dignity', 'typings']
	d['num_pep'] = len(peptides)
	d['num_runs'] = len(ms_stack)
	table.append(d)
	return table


def fastPeptidesTable(DBSession, Peptide, Hit, SourceData, SourceHLA, HLAAllele, PrepData, Mass_specData, Person, peptides) :
	table = []
	i = 0
	for hit in DBSession.query(Hit).all() :
		if DBSession.query(Peptide).get(hit.peptide_peptide_id) in peptides :
			i = i + 1
			d = dict()
			d['Nr'] = i
			d['Sequence'] = DBSession.query(Peptide).get(hit.peptide_peptide_id).sequence
			d['E-value'] = hit.e_value
			d['Person'] = getPersonById_Name(DBSession, Person, DBSession.query(Mass_specData).get(hit.ms_run_ms_run_id).person_person_id)
			
			d['Source'] = DBSession.query(SourceData).get(DBSession.query(Mass_specData).get(hit.ms_run_ms_run_id).source_source_id).name
			d['Dignity'] = DBSession.query(SourceData).get(DBSession.query(Mass_specData).get(hit.ms_run_ms_run_id).source_source_id).dignity
		
			typings = getTypingsBySourceId(DBSession, SourceHLA, DBSession.query(SourceData).get(DBSession.query(Mass_specData).get(hit.ms_run_ms_run_id).source_source_id).source_id)
			types = []
			for i in range(0, len(typings)) :
				type = ''
				type += DBSession.query(HLAAllele).get(typings[i].hlaallele_hlaallele_id).gene_group
				if not typings[i].specific_protein is None : #XXX to test
					type += ':'
					type += typings[i].specific_protein
					if not typings[i].dna_coding is None :
						type += ':'
						type += typings[i].dna_coding
						if not typings[i].dna_noncoding is None :
							type += ':'
							type += typings[i].dna_noncoding
							if not typings[i].expession_suffix is None :
								type += typings[i].expession_suffix
				types.append(type)
			#prep = DBSession.query(PrepData).get(ms_run.mhcpraep_mhcpraep_id)
			d = dict()
			d['typings'] = types
			table.append(d)
			
			
	d = dict()
	d['cols'] = ['Nr', 'Sequence', 'E-value',  'Person', 'Source', 'Dignity', 'typings']#, 'e_value', 'person_run', 'source_name', 'source_dignity', 'typings']
	d['Number of hits'] = i
	d['Number of peptides'] = len(peptides)
	#d['Number of '] = len(ms_stack)
	table.append(d)
	return table
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	