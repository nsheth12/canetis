import csv

test_file_path = "../kelly_qtype_csvs/2-Adrian-5-Transcript.csv"
f = open(test_file_path, "r")
reader = csv.reader(f)

question_col = 0
answer_col = 1
rowcount = 0
next(reader)
for row in reader:
	if rowcount < 10:
		row_list = list(row)
		print(row_list[question_col].split("Q:")[1].strip())
		print(row_list[answer_col].split("A:")[1].strip())
	rowcount += 1
