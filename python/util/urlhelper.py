def attach_links(link_start, dict_list):
    for dict in dict_list:
        dict["url"] = link_start+str(dict["id"])
