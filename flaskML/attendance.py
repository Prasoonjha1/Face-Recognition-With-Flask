import pandas as pd
import datetime
import numpy as np
import config

def mark_attendance(name):
    df = pd.read_csv('Attendance.csv')
    if name!='unknown':
        ind = 0
        for nam in df['Roll No.']:
            if nam == name:
                print(str(ind)+":"+nam)
                config.nameList[ind] = 'P'
            ind+1
        date_time_string = datetime.datetime.now().strftime("%d/%m/%y")
        df[date_time_string] = config.nameList[::-1]
        df.to_csv("Attendance.csv", index=False)
