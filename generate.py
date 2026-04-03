import csv
import random

file = open("students_4000.csv","w",newline="")
writer = csv.writer(file)

writer.writerow(["roll_number","name","branch","year"])

years = [
("E1","23"),
("E2","22"),
("E3","21"),
("E4","20")
]

branches = [
("CSE",360),
("ECE",300),
("MECH",200),
("CIVIL",140)
]

for year_label,batch in years:

    counter = 1000

    for branch,total in branches:

        for i in range(total):

            roll = f"RO{batch}{counter}"
            name = f"Student_{counter}"

            writer.writerow([roll,name,branch,year_label])

            counter += 1

file.close()

print("CSV created successfully")