#this tool generate phoible_specific language from whole phoible csv
#to use this same phoible.csv in the folder and change line 22 to your desired language. 

import csv
import os

def filter_phoible_by_iso(iso_code, input_file='phoible.csv', output_folder='.'):
    output_file = os.path.join(output_folder, f'phoible_{iso_code}.csv')
    
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            if row['ISO6393'] == iso_code:
                writer.writerow(row)

#change ISO6393 code here, e.g."eng"
iso_code = "deu"
filter_phoible_by_iso(iso_code.strip())
print(f"generated: phoible_{iso_code}.csv")