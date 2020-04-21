import os, sqlite3
from flask import g
from application import Config, app

DATABASE = os.path.join(Config.BASE_DIR, "application/static/processing/hsbctrtoolkit.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        #db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

#db.row_factory = make_dicts

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def write_db(query, args, msg_var):
    try:
        cur = get_db().execute(query, args)
        get_db().commit()
        msg = f"Record {msg_var} successfully!"
    except:
        get_db().rollback()
        msg = f"Error in {msg_var} record!"
    finally:
        cur.close()
        return msg

def truncate_db(query, args=()):
    try:
        cur = get_db().execute(query, args)
        get_db().commit()
        msg = "Record deleted successfully!"
    except:
        get_db().rollback()
        msg = "Error in deleting record!"
    finally:
        cur.close()
        return msg


def insert_or_update_progress():
    query = "SELECT current_count, total_fn_count from script_progress WHERE script_id = ?"
    rv = query_db(query, [1], one=True)
    if rv is None:
        insert_query = "INSERT INTO script_progress (script_id, current_count, total_fn_count) VALUES (?,?,?)"
        insert_args = (1,0,2)
        msg = write_db(insert_query,insert_args,"added")
        print(msg)
    else:
        up_qry = "UPDATE script_progress SET current_count = ?, total_fn_count = ? WHERE script_id = ?"
        up_args = (0,2,1)
        msg = write_db(up_qry, up_args,"updated")
        print(msg)

        