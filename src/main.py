import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import connect_db, get_db_engine
from fear_greed_index import get_df_fg_index_today
from constants import fg_today_url

def create_fg_index_table():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS fear_greed_index (
                   id SERIAL PRIMARY KEY,
                   fg_index_num INTEGER NOT NULL,
                   fg_index_str VARCHAR(20) NOT NULL,
                   date_index DATE NOT NULL,
                   time_until_update VARCHAR(30) NOT NULL
                   )""")
    connection.commit()
    cursor.close()
    connection.close()

create_fg_index_table()
df = get_df_fg_index_today(fg_today_url)
engine = get_db_engine()
df.to_sql('fear_greed_index', engine, if_exists='append', index=False)