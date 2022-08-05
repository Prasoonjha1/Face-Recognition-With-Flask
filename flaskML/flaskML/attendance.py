from datetime import datetime
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDat = f.readlines()
        nameList = []
        ind=0
        for line in myDat:
            entry = line.split(',')
            nameList.append(entry[1])
            if entry[0] != 'S.No.':
                ind = entry[0]
        if name not in nameList:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{int(ind)+1},{name},{dtstring}')
