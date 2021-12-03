from neomodel import db

names = db.cypher_query(
    '''
    MATCH (n)
    RETURN DISTINCT n.name AS name
    '''
)[0]

NAMES = names

comparisons = db.cypher_query(
    '''
    match (x)<-[:HAS_ENTITY|:HAS_KEYPHRASE]-(s1:Story)
    match (x)<-[:HAS_ENTITY|:HAS_KEYPHRASE]-(s2:Story)
    where s1 <> s2
    and s1.nodeID < s2.nodeID
    with  s1 as s1, s2 as s2, count(distinct x) as shared, collect(distinct x.text) as stuff
    order by shared desc
    return s1.name, collect(s2.name)[0], stuff
    '''
)[0]

COMPARISON = comparisons
