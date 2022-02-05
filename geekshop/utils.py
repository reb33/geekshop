def db_profile_by_type(prefix, type_query, queries):
    update_queries = filter(lambda x: type_query in x['sql'], queries)
    print(f'db_profile {type_query} for {prefix}:')
    [print(query['sql']) for query in update_queries]