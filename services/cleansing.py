import pandas as pd
from collections import Counter
from libs.nlp import preprocess_tweets, preprocess_file
from services import AppServiceProject
from io import BytesIO
from fastapi.responses import StreamingResponse
import io
import sqlite3
 
class CleansingServices(AppServiceProject):
    async def cleansing(self, type, text):
        try:
            if type == "text":
                preprocess = preprocess_tweets(text)
 
                data = {
                "data": preprocess
                }
 
                return self.success_response(data)
            else:
                preprocess = preprocess_file(text)
                
                conn = sqlite3.connect("data/tweets_hasil.db")
                conn.execute('''create table tweets (tweet varchar(500), HS int,
                                Abusive int, HS_individual int, HS_group int, HS_religion int, HS_race int,
                                HS_physical int, HS_gender int, HS_other int, HS_weak int, HS_moderate int, 
                                HS_strong int);''')
                
                preprocess.to_sql('tweets', conn, if_exists= 'replace', index= False)
                conn.commit()
                conn.close()

                stream = io.StringIO()
                preprocess.to_csv(stream, index = False)
 
                response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
                            )
                response.headers["Content-Disposition"] = "attachment; filename=export.csv"
 
                return response            
        except Exception as e:
            return self.error_response(e)