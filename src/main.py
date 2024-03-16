import os, time
import pandas as pd
from process_data import process_data
from db import initialize_db, insert_events_data
from dotenv import load_dotenv
load_dotenv()

def main_pipeline():
    src_data_path = os.path.join(os.getcwd(), "sample_data", "KSP_hackathon_data.xlsx")
    db_path = initialize_db()

    try:
        src_data_df = pd.read_excel(src_data_path)
        
        for index,row in src_data_df.iterrows():
            print('Processing Record', index)
            result_dict = process_data(row['Post'],row['Timestamp'])
            #print(result_dict)
            if result_dict == False:
                return False
            insert_events_data(result_dict,db_path)
            print('Processed Record', index)
            time.sleep(30)
        return True
    
    except Exception as e:
        print('Error:', str(e))
        return False
        


if __name__ == "__main__":
    if main_pipeline():
        print('Success')
