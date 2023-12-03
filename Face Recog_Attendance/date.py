from datetime import datetime
import csv
import os

date_t=datetime.today()
datet=date_t.strftime("%d/%b/%Y")
print(datet)
name="Attendance_"+datet+".csv"
name_t=(str(name))
lsitt=['1','2',4,5,6,7]
with open("Attendance1.csv",'w',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(lsitt)
f.close()
import shutil

Current_Date = datetime.today().strftime('%d-%b-%Y')

shutil.copyfile(r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton\Attendance.csv',
                        r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton\Attendance_' + str(Current_Date) + '.csv')
# Absolute path of a file

# old_name = r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton\Attendance1.csv'
# new_name = 'Attendance'+datet+'.csv'
# Current_Date = datetime.today().strftime ('%d-%b-%Y')
# Renaming the file
# os.rename(r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton\Attendance1.csv',r'C:\Users\Lenovo\PycharmProjects\FaceRecogniton\Attendance_' + str(Current_Date) + '.csv')
file = 'Attendance.csv'
lines = open(file).readlines()
open(file, 'w').writelines(lines[:2])