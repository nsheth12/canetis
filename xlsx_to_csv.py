import os, subprocess, sys


def get_file_names(back_up_path):
	return os.listdir(back_up_path)


def get_csv(xlsx):
	csv = xlsx
	csv = csv.split(".")
	csv[-1] = "csv"
	csv = ".".join(csv)
	return csv


xlsx_path = sys.argv[1] 
end_path = sys.argv[2]



xlsx_files = get_file_names(xlsx_path)


	

for xlsx in xlsx_files:
	xlsx_path = xlsx_path+"/"+ xlsx	
	print(xlsx_path)
	csv_path = end_path+"/" +get_csv(xlsx)
	subprocess.call(["touch", csv_path])
	subprocess.call(["ssconvert", xlsx_path, csv_path])


	
