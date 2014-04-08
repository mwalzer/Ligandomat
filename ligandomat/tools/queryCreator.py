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
        filter_string += " sequence LIKE '"+search_dict["sequence_input"]+"'"
        first = False
    # Run name
    if "run_name_input" in search_dict.keys():
        if first:
            filter_string += " filename LIKE '"+search_dict["run_name_input"]+"'"
        else:
            filter_string += " AND filename LIKE '"+search_dict["run_name_input"]+"'"
    # Source
    # Source name
    if "source_name_input" in search_dict.keys():
        if first:
            filter_string += " name LIKE '"+search_dict["source_name_input"]+"'"
        else:
            filter_string += " AND name LIKE '"+search_dict["source_name_input"]+"'"
    # Organ
    if "organ_input" in search_dict.keys():
        if first:
            filter_string += " organ LIKE '"+search_dict["organ_input"]+"'"
        else:
            filter_string += " AND organ LIKE '"+search_dict["organ_input"]+"'"
    # Tissue
    if "tissue_input" in search_dict.keys():
        if first:
            filter_string += " tissue LIKE '"+search_dict["tissue_input"]+"'"
        else:
            filter_string += " AND tissue LIKE '"+search_dict["tissue_input"]+"'"
    # Dignity
    if "dignity_input" in search_dict.keys():
        if first:
            filter_string += " dignity LIKE '"+search_dict["dignity_input"]+"'"
        else:
            filter_string += " AND dignity LIKE '"+search_dict["dignity_input"]+"'"
    # Dignity
    if "researcher_input" in search_dict.keys():
        if first:
            filter_string += " lastname LIKE '"+search_dict["researcher_input"]+"'"
        else:
            filter_string += " AND lastname LIKE '"+search_dict["researcher_input"]+"'"
    # Source HLA typing
    if "source_hla_typing_input" in search_dict.keys():
        # TODO: gene_group can be a list or something so a like check is not feasiable.
        if first:
            filter_string += " gene_group LIKE '"+search_dict["source_hla_typing_input"]+"'"
        else:
            filter_string += " AND gene_group LIKE '"+search_dict["source_hla_typing_input"]+"'"

    filter_string += " AND ionscore > " + str(search_dict["ionscore_input"])\
                     + " AND e_value < " + str(search_dict["e_value_input"])\
                     + " AND q_value < " + str(search_dict["q_value_input"])\
                     + " GROUP BY sourcename"

    return filter_string

    """
    # Sequence
    if "sequence_input" in search_dict.keys():
        query_dict["peptide"] = "WHERE sequence LIKE '"+search_dict["sequence_input"]+"'"
    else:
        query_dict["peptide"] = ""

    # Run name
    if "run_name_input" in search_dict.keys():
        query_dict["ms_run"] = "WHERE filename LIKE '"+search_dict["run_name_input"]+"'"
    else:
        query_dict["ms_run"] = ""

    # Source name
    if "source_name_input" in search_dict.keys():
        query_dict["source_name"] = "WHERE name LIKE '"+search_dict["source_name_input"]+"'"
    else:
        query_dict["source_name"] = ""

    # Source
    where_set = False
    if "source_name_input" in search_dict.keys():
        query_dict["source"] = "WHERE name LIKE '" + search_dict["source_name_input"]+"'"
        where_set = True

    if "organ_input" in search_dict.keys():
        if where_set:
            query_dict["source"] = query_dict["source"]+"AND organ LIKE '"+search_dict["organ_input"]+"'"
        else:
            query_dict["source"] = "WHERE organ LIKE '"+search_dict["organ_input"]+"'"

    if "tissue_input" in search_dict.keys():
        if where_set:
            query_dict["source"] = query_dict["source_input"]+"AND tissue LIKE '"+search_dict["tissue_input"]+"'"
        else:
            query_dict["source"] = "WHERE tissue LIKE '"+search_dict["tissue_input"]+"'"

    if "dignity_input" in search_dict.keys():
        if where_set:
            query_dict["source"] = query_dict["tissue_input"]+"AND dignity LIKE '"+search_dict["dignity_input"]+"'"
        else:
            query_dict["source"] = "WHERE dignity LIKE '"+search_dict["dignity_input"]+"'"
    if not where_set:
        query_dict["source"] = ""

    # Researcher
    if "researcher_input" in search_dict.keys():
        query_dict["person"] = "WHERE lastname LIKE '"+search_dict["researcher_input"]+"'"
    else:
        query_dict["person"] = ""

    # Source HLA typing
    if "source_hla_typing_input" in search_dict.keys():
        query_dict["source_hla_typing"] = ""
        #TODO :queryDict["source_hla_typing"] = "source_hla_typing organ LIKE"+params.get("source_hla_typing")
    else:
        query_dict["source_hla_typing"] = ""

    query_dict["spectrum_hit"] = "WHERE ionscore > " + str(search_dict["ionscore_input"]) + " AND e_value < " \
                                 + str(search_dict["e_value_input"]) + " AND q_value < " + str(search_dict["q_value_input"])



    return query_dict
    """