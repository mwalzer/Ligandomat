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
        # TODO: gene_group can be a list or something so a like check is not feasiable.
        source_hla_typing_input = search_dict["source_hla_typing_input"].split(";")
        # if it is not first an "AND" must be added
        if first:
            filter_string += " ( "
            first = False
        else:
            filter_string += " AND ( "
        # combining the input
        for i, source_hla_typing in enumerate(source_hla_typing_input):
            if i != len(source_hla_typing_input)-1:
                filter_string += " source_hla_typing LIKE '" + researcher.strip() + "' " + search_dict["source_hla_typing_logic"]
            else:
                filter_string += " source_hla_typing LIKE '" + researcher.strip() + "' "
        filter_string += ") "

    filter_string += " AND ionscore > " + str(search_dict["ionscore_input"]) \
                     + " AND e_value < " + str(search_dict["e_value_input"]) \
                     + " AND q_value < " + str(search_dict["q_value_input"]) \
                     + " GROUP BY sequence"

    return filter_string