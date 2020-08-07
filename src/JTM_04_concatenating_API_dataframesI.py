import re
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # loading file
    print('loading file')
    df_all = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\02_ListaPiosenekAllClean.xlsx')

    row_count = len(df_all.index)
    number_of_items = 500
    number_of_intervals = round(row_count / number_of_items)

    df_all = []
    for value in range(0, number_of_intervals + 1):
        if value == 0:
            start_number = value * number_of_items
        else:
            start_number = value * number_of_items + 1
        end_number = value * number_of_items + number_of_items

        # loading partial file
        df_partial = pd.read_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\interim\deezer_API\03_ListaPiosenek_{start}-{end}.xlsx'.format(start=start_number, end=end_number))

        # adding partial file to list
        df_all.append(df_partial)

    df_all = pd.concat(df_all, axis=0, sort=False)

    # saving to excel file
    print('saving file')
    df_all.to_excel(r'C:\Users\kose9001\Desktop\JakaToMelodia\data\processed\04_ListaPiosenekAPIClean.xlsx', index=False, encoding='ISO-8859-1')

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

if __name__ == "__main__":
    main()


