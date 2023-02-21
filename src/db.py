import re
import sqlite3

db_file = 'translate_cache.db'
columns = ['source', 'target', 'original', 'translation']

con = sqlite3.connect(db_file)
cur = con.cursor()

# ensure string is safe for sqlite
def ensure_safe_string(string):
    pattern = r"[^0-9a-zA-Z_]"
    cleaned_string = re.sub(pattern, "", string)
    return cleaned_string

# ensure table exists
def trdb_ensure_table_exists(table_name):
    table_name = ensure_safe_string(table_name)
    cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name=?', (table_name,))
    if cur.fetchone() is None:
        print('Creating table: {}'.format(table_name))
        cur.execute('CREATE TABLE {} (source TEXT NOT NULL, target TEXT NOT NULL, original TEXT NOT NULL, translation TEXT NOT NULL)'.format(table_name))
        # create index (query priority: original, target, source)
        cur.execute('CREATE UNIQUE INDEX {} ON {} (original, target, source)'.format(table_name + '_index', table_name))
        con.commit()

# insert a row
def trdb_insert_batch(table_name, values_list):
    table_name = ensure_safe_string(table_name)
    cur.executemany('INSERT INTO {} VALUES (?, ?, ?, ?)'.format(table_name), (values_list))
    con.commit()

# insert if (source, target, original) key not exists or update a row
def trdb_insert_or_update_batch(table_name, value_dict_list):
    table_name = ensure_safe_string(table_name)
    # check if row exists
    for value_dict in value_dict_list:
        cur.execute('SELECT * FROM {} WHERE source=? AND target=? AND original=?'.format(table_name),
            (value_dict['source'], value_dict['target'], value_dict['original']))
        exists = cur.fetchone()
        if exists is None:
            # insert
            cur.execute('INSERT INTO {} VALUES (?, ?, ?, ?)'.format(table_name),
                (value_dict['source'], value_dict['target'], value_dict['original'], value_dict['translation']))
        else:
            # update
            cur.execute('UPDATE {} SET translation=? WHERE source=? AND target=? AND original=?'.format(table_name),
                (value_dict['translation'], value_dict['source'], value_dict['target'], value_dict['original']))
    con.commit()

# find a row that matches the 'source', 'target', 'original' values
def trdb_find(table_name, value_dict):
    table_name = ensure_safe_string(table_name)
    cur.execute('SELECT * FROM {} WHERE source=? AND target=? AND original=?'.format(table_name),
        (value_dict['source'], value_dict['target'], value_dict['original']))
    row = cur.fetchone()
    # return as dict
    if row is not None:
        return dict(zip(columns, row))
    else:
        return None

# query rows with offset and limit
def trdb_query(table_name, opt_dict = {}):
    limit = opt_dict.get('limit', 100)
    offset = opt_dict.get('offset', 0)

    table_name = ensure_safe_string(table_name)
    cur.execute('SELECT * FROM {} LIMIT ? OFFSET ?'.format(table_name), (limit, offset))
    rows = cur.fetchall()
    # return as list of dict
    return [dict(zip(columns, row)) for row in rows]
