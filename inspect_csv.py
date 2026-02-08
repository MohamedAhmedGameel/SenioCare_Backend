import csv

files = {
    'disease_information': 'DDID Database/disease_information_preprocessed.csv',
    'drug_information': 'DDID Database/drug_information_preprocessed.csv',
    'food_information': 'DDID Database/food_information_preprocessed.csv',
    'herb_information': 'DDID Database/herb_information_preprocessed.csv',
    'drug_foodherb_interaction': 'DDID Database/drug_foodherb_interaction_preprocessed.csv'
}

for name, filepath in files.items():
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print(f'\n{name}:')
        print(f'Columns: {reader.fieldnames}')
        
        # Get first row
        try:
            row = next(reader)
            print(f'\nSample data (first 5 fields):')
            for i, (k, v) in enumerate(list(row.items())[:10]):
                value = str(v)[:80] if v else ''
                print(f'  {k}: {value}')
        except StopIteration:
            print('  No data rows found')
