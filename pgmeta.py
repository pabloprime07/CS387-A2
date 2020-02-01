import psycopg2
import dbexec
from dbmeta import Meta, Table, Column

def get_meta_data(conn):
    """Populates a dbmeta.Meta object with Tables, Columns and inter-Table relationships"""
    meta = Meta()
    load_columns(conn, meta)  # Same query as exercise 1.
    constraints = load_constraints(conn) # constraint_name -> table mapping
    load_relationships(conn, meta, constraints)
    return meta

def load_columns(conn, meta: Meta):
    c = conn.cursor()
    query = """SELECT distinct C.table_name, C.column_name, case B.constraint_type 
    when 'PRIMARY KEY' then '*'
    when 'FORIEGN KEY' then ''
    end as is_pk, 
  C.data_type from information_schema.columns C
FULL OUTER JOIN ( select distinct K.column_name, T.constraint_type from information_schema.key_column_usage as K, information_schema.table_constraints as T where K.constraint_name = T.constraint_name and T.constraint_type='PRIMARY KEY'
) as B ON B.column_name=C.column_name 
where table_schema='public'
order by table_name;
    """
    (header, rows) = dbexec.exec_query(conn, query)
    for row in rows:
        if row[0] in meta.tables:
            # m.tables[tbl.name] = tbl
            meta.tables[row[0]].columns.append(Column(name=row[1], table = row[0], data_type = row[3], is_pk = row[2]))
        else:
            # Table t
            t = Table(name=row[0])
            t.columns.append((Column(name=row[1], table = row[0], data_type = row[3], is_pk = row[2])))
            meta.tables[row[0]] = t
        # TODO: create Table and Column objects and attach to meta. 
    c.close()

def load_constraints(conn):
    table_constraints = dict() # Map of constraint name -> containing table name
    c = conn.cursor()
    query = """select constraint_name, table_name from information_schema.table_constraints where table_schema='public';"""
    (header, rows) = dbexec.exec_query(conn, query)
    # TODO: Load table_constraints table for primary and foreign keys, and record
    # the constraint_table and the containing table name.
    for row in rows:
        table_constraints[row[0]] = row[1]
    c.close()
    return table_constraints

def load_relationships(conn, meta, constraints):
    c = conn.cursor()

    # TODO : query referential_constraints table, which maps constraint in one table
    #      : to unique constraint in another table
    # TODO : for each row create meta.tables[from_table].refersTo += meta.tables[to_table]
    query = """select constraint_name, unique_constraint_name from information_schema.referential_constraints  ;"""
    (header, rows) = dbexec.exec_query(conn, query);
    for row in rows:
        meta.tables[constraints[row[0]]].refersTo.append(meta.tables[constraints[row[1]]])
    c.close()
    
def to_graph(meta):
    str = ""
    for tbl in meta.tables.values():
        str += "[" + tbl.name + "|"
        str += "|".join([col.name for col in tbl.columns])
        str += "]\n"
        for t in tbl.refersTo:
            str += "[%s] -> [%s]\n"%(tbl.name, t.name)
    return str

if __name__ == "__main__":
    import config
    conn = dbexec.connect()
    meta = get_meta_data(conn) # returns dbmeta 'Meta'
    conn.close()
    print(to_graph(meta))
