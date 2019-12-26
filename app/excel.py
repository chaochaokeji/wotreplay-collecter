import os
import xlsxwriter
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')

def main():
    if os.path.exists('players.xlsx'):
        os.remove('players.xlsx')
    workbook = xlsxwriter.Workbook('players.xlsx')
    worksheet = workbook.add_worksheet()
    playersCol = client['wotreplay-collecter']['players']
    i = 1
    for player in playersCol.find():
        worksheet.write('A' + str(i), player['id'])
        worksheet.write('B' + str(i), player['name'])
        worksheet.write('C' + str(i), player['clan'])
        worksheet.write('D' + str(i), player['serverName'])
        worksheet.write('E' + str(i), player['vehicle'])
        worksheet.write('F' + str(i), player['dateTime'])
        i += 1
    workbook.close()

if __name__ == '__main__':
    main()