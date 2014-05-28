__author__ = 'linus'


def create_query(search_dict):
    """ Creates a query parts dictionary

    :search_dict search_dict:

    Dict contains:
        peptide
        ms_run
        source_name
        source (organ/tissue/dignity)
        person
        source_hla_typing (TODO)
        spectrum_hit (ionscore, e-value, q-value)
        """
    #query_dict = dict()
    filter_string = "WHERE"
    first = True

    # Sequence
    if "sequence_input" in search_dict.keys():
        sequence_input = search_dict["sequence_input"].split(";")
        filter_string += " ( "

        # combining the query
        for i, seq in enumerate(sequence_input):
            if i != len(sequence_input) - 1:
                filter_string += " sequence LIKE '" + seq.strip() + "' " + search_dict["sequence_logic"]
            else:
                filter_string += " sequence LIKE '" + seq.strip() + "' "

        # OR needs brackets (closing bracket)
        filter_string += ") "
        first = False

    # Run name
    if "run_name_input" in search_dict.keys():
        run_name_input = search_dict["run_name_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, run in enumerate(run_name_input):
            if i != len(run_name_input) - 1:
                filter_string += " filename LIKE  '" + run.strip() + "' " + search_dict["run_name_logic"]
            else:
                filter_string += " filename LIKE  '" + run.strip() + "' "
        filter_string += ") "

    # Source
    # Source name
    if "source_name_input" in search_dict.keys():
        source_name_input = search_dict["source_name_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, source in enumerate(source_name_input):
            if i != len(source_name_input) - 1:
                filter_string += " name LIKE '" + source.strip() + "' " + search_dict["source_name_logic"]
            else:
                filter_string += " name LIKE '" + source.strip() + "' "
        filter_string += ") "

    # Organ
    if "organ_input" in search_dict.keys():
        organ_input = search_dict["organ_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, organ in enumerate(organ_input):
            if i != len(organ_input) - 1:
                filter_string += " organ LIKE '" + organ.strip() + "' " + search_dict["organ_logic"]
            else:
                filter_string += " organ LIKE '" + organ.strip() + "' "
        filter_string += ") "

    # Tissue
    if "tissue_input" in search_dict.keys():
        tissue_input = search_dict["tissue_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, tissue in enumerate(tissue_input):
            if i != len(tissue_input) - 1:
                filter_string += " tissue LIKE '" + tissue.strip() + "' " + search_dict["tissue_logic"]
            else:
                filter_string += " tissue LIKE '" + tissue.strip() + "' "
        filter_string += ") "

    # Dignity
    if "dignity_input" in search_dict.keys():
        dignity_input = search_dict["dignity_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, dignity in enumerate(dignity_input):
            if i != len(dignity_input) - 1:
                filter_string += " dignity LIKE '" + dignity.strip() + "' " + search_dict["dignity_logic"]
            else:
                filter_string += " dignity LIKE '" + dignity.strip() + "' "
        filter_string += ") "

    # Dignity
    if "researcher_input" in search_dict.keys():
        researcher_input = search_dict["researcher_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, researcher in enumerate(researcher_input):
            if i != len(researcher_input)-1:
                filter_string += " lastname LIKE '" + researcher.strip() + "' " + search_dict["researcher_logic"]
            else:
                filter_string += " lastname LIKE '" + researcher.strip() + "' "
        filter_string += ") "

    # Source HLA typing
    if "source_hla_typing_input" in search_dict.keys():
        source_hla_typing_input = search_dict["source_hla_typing_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, source_hla_typing in enumerate(source_hla_typing_input):
            hla_type = source_hla_typing.strip().split(':')
            # Basic gene group (2 digits)
            hla_query = "( gene_group = '" + hla_type[0].strip() + "' "
            # Protein (4 digits)
            if len(hla_type) > 1:
                hla_query += " AND " + " specific_protein = " + str(int(hla_type[1].strip()))
            # DNA coding (6 digits)
            if len(hla_type) > 2:
                hla_query += " AND " + " dna_coding =  " + str(int(hla_type[2].strip()))
            # DNA non-coding (8 digits)
            if len(hla_type) > 3:
                # Expression suffix (extra char suffix)
                if hla_type[3].strip()[-1].isalpha():
                    hla_query += " AND " + " dna_noncoding = " + str(int(hla_type[3].strip()[:-1])) + " AND expression_suffix == '" + hla_type[3].strip()[-1] + "' "
                else:
                    hla_query += " AND " + " dna_noncoding = " + str(int(hla_type[3].strip()))
            # creating the query. If more than one typing is provided they are combined
            if i != len(source_hla_typing_input)-1:
                filter_string += hla_query + ") " + search_dict["source_hla_typing_logic"]
            else:
                filter_string += hla_query + ") "
        filter_string += ") "

    # Protein
    if "protein_input" in search_dict.keys():
        protein_input = search_dict["protein_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, protein in enumerate(protein_input):
            if i != len(protein_input)-1:
                filter_string += " uniprot_accession_pm LIKE '" + protein.strip() + "' " + search_dict["protein_logic"]
            else:
                filter_string += " uniprot_accession_pm LIKE '" + protein.strip() + "' "
        filter_string += ") "
    # netMHC prediction

    if "netMHC_input" in search_dict.keys():
        netMHC_information = search_dict["netMHC_information"].replace("*", "_").replace(":", "_").split(";")
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, allele in enumerate(netMHC_information):
            if i != len(netMHC_information)-1:
                filter_string+= " Prediction_mapping.netMHC_3_4."+allele+"_affinity"+search_dict["netMHC_comparison"]+search_dict["netMHC_input"]+" "+ search_dict["netMHC_logic"]+" "
            else:
                filter_string += "Prediction_mapping.netMHC_3_4."+allele+"_affinity"+search_dict["netMHC_comparison"]+search_dict["netMHC_input"]+" "
        filter_string += ") "

    # syfpeithi prediction
    if "syfpeithi_input" in search_dict.keys():
        syfpeithi_information = search_dict["syfpeithi_information"].replace("*", "_").replace(":", "_").split(";")
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, allele in enumerate(syfpeithi_information):
            if i != len(syfpeithi_information)-1:
                filter_string+= " Prediction_mapping.syfpeithi_170414."+allele+"_affinity"+search_dict["syfpeithi_comparison"]+search_dict["syfpeithi_input"] + " " + search_dict["syfpeithi_logic"]+" "
            else:
                filter_string += "Prediction_mapping.syfpeithi_170414."+allele+"_affinity"+search_dict["syfpeithi_comparison"]+search_dict["syfpeithi_input"] + " "
        filter_string += ") "

    # Standard filters
    filter_string += " AND ionscore >= " + str(search_dict["ionscore_input"]) \
                     + " AND q_value <= " + str(search_dict["q_value_input"]) \
                     + " AND LENGTH(sequence) BETWEEN "+ str(search_dict["aa_length_start"])\
                     + " AND " + str(search_dict["aa_length_end"])\
                     + " GROUP BY filename, sequence"

    return filter_string


