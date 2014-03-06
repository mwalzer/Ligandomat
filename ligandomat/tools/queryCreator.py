__author__ = 'linus'



def create_query(params):
    """ Creates a query parts dictionary

        Dict contains:
            sequence
            run_name
            source_name
            source (organ/tissue/dignity)
            researcher
            source_hla_typing (TODO)
            spectrum_hit (ionscore, e-value, q-value)
        """
    query_dict = dict()

    # Sequence
    if "sequence" in params:
        query_dict["peptide"] = "WHERE sequence LIKE "+params.get("sequence")
    else:
        query_dict["peptide"] = ""

    # Run name
    if "run_name" in params:
        query_dict["ms_run"] = "WHERE filename LIKE "+params.get("run_name")
    else:
        query_dict["ms_run"] = ""

    # Source name
    if "source_name" in params:
        query_dict["source_name"] = "WHERE name LIKE "+params.get("source_name")
    else:
        query_dict["source_name"] = ""

    # Source
    where_set = False
    if "source_name" in params:
        query_dict["source"] = "WHERE name LIKE " + params.get("source_name")
        where_set = True

    if "organ" in params:
        if where_set:
            query_dict["source"] = query_dict["source"]+"AND organ LIKE "+params.get("organ")
        else:
           query_dict["source"] = "WHERE organ LIKE "+params.get("organ")

    if "tissue" in params:
        if where_set:
            query_dict["source"] = query_dict["source"]+"AND tissue LIKE "+params.get("tissue")
        else:
           query_dict["source"] = "WHERE tissue LIKE "+params.get("tissue")

    if "dignity" in params:
        if where_set:
            query_dict["source"] = query_dict["tissue"]+"AND dignity LIKE "+params.get("dignity")
        else:
           query_dict["source"] = "WHERE dignity LIKE "+params.get("dignity")
    if not where_set:
        query_dict["source"] = ""

    # Researcher
    if "researcher" in params:
        query_dict["person"] = "WHERE lastname LIKE "+params.get("researcher")
    else:
        query_dict["person"] = ""

    # Source HLA typing
    if "source_hla_typing" in params:
        query_dict["source_hla_typing"] = ""
        #TODO :queryDict["source_hla_typing"] = "source_hla_typing organ LIKE"+params.get("source_hla_typing")
    else:
        query_dict["source_hla_typing"] = ""

    query_dict["spectrum_hit"] = "WHERE ionscore > " + str(params.get("ion_score")) + " AND e_value < " \
                                 + str(params.get("e-value")) + " AND q_value < " + str(params.get("q-value"))



    return query_dict