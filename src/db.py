import sqlite3, click, os, gdown, csv
from flask import current_app, g



def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db



def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

    

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    click.echo('Initialized the database.')

    click.echo('Downloading data.csv...')
    gdown.download(
        'https://drive.google.com/file/d/1q3Kk0304oGouHwKR_XWVBBLmaPc8AV6s/view?usp=drive_link',
        'data.csv', 
        fuzzy=True
    )
    with open('data.csv', 'r', encoding="utf8") as f:
        cursor = db.cursor()
        data = csv.reader(f, delimiter=',')
        for row in data:
            cursor.execute("""
                INSERT INTO PlantDisease (disease_id, plant_name, disease_name, affect, solution) 
                VALUES (?, ?, ?, ?, ?)
            """, row)
        db.commit()
    click.echo('Added data to the database.')
    os.remove('data.csv')



@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)