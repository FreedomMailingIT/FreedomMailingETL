"""
Untangle mailing addresses given as multi-line, multi-column spreadsheet
"""

import csv


def reformat_label(raw):
    """re-arrange address"""
    name = address = city = state = pzip = ''
    for line in raw:
        name += line[0]
        address += line[1]
        if line[2]:
            city += line[2]
            state += line[3].replace('<null>', '')
            pzip += line[4].replace('<null>', '')
    return [name, address, city, state, pzip]


def main():
    """Read records into memory and re-arrange"""
    path = '/Users/gjbak/Downloads/freedommailing/'
    fname = 'Parcels to be Withdrawn.csv'

    source = open(path+fname, 'rU', encoding='utf-8')
    dest = open(path+'fxd '+fname, 'w', encoding='utf-8')

    in_data = csv.reader(source)
    out_data = csv.writer(dest, quoting=csv.QUOTE_ALL, lineterminator='\n')
    label = []
    for row in in_data:
        if row[4] and label:
            label = reformat_label(label)
            out_data.writerow(label)
            label = []
        label.append(row)

    source.close()
    dest.close()


if __name__ == '__main__':
    main()
