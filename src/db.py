import sqlite3, os


def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    return conn


def create_tables(db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    try:
        events_data_create = '''
                        CREATE TABLE IF NOT EXISTS tbl_events_data(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            post_content TEXT NOT NULL,
                            event_place TEXT,
                            timestamp TEXT,
                            sentiment TEXT CHECK(sentiment IN ('Positive', 'Negative', 'Neutral')),
                            event_type TEXT CHECK(event_type IN ('Accident', 'Violence', 'Riot')),
                            severity TEXT CHECK(severity IN ('High', 'Medium', 'Low')),
                            hashtags TEXT,
                            log_time DATETIME DEFAULT CURRENT_TIMESTAMP)
                    '''

        cursor.execute(events_data_create)
        conn.commit()

        conn.close()
        return True

    except Exception as e:
        print("Error:",str(e))
        conn.close()
        return False


def insert_data_init(db_path):
    return True


def insert_events_data(data_dict, db_path):
    conn = connect_db(db_path)
    cursor = conn.cursor()
    query = f'''
                INSERT INTO tbl_events_data(post_content, event_place,timestamp, sentiment, event_type, severity, hashtags)
                VALUES("{data_dict['post_content'].replace("'","''")}","{data_dict['event_place'].replace("'","''")}",
                "{data_dict['timestamp'].strftime(('%Y-%m-%d %H:%M:%S'))}",
                "{data_dict['sentiment'].value}", "{data_dict['event_type'].value}",
                "{data_dict['severity'].value}", "{data_dict['hashtags'].replace("'","''")}")
            '''
    try:
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(query)
        print(str(e))
        conn.close()
        return False
    
    


def initialize_db():
    db_directory = os.path.join(os.getcwd(), "sample_data")
    db_file = os.path.join(db_directory, "data.db")

    if os.path.isfile(db_file):
        return db_file
    
    if not create_tables(db_file):
        return False
    
    if not insert_data_init(db_file):
        return False
    
    return db_file