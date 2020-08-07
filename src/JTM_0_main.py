import pandas as pd
import time
import JTM_06_lastfm_API
import JTM_07_fuzzywuzzy_match_2
import JTM_08_fuzzywuzzy_match_3
import JTM_09_deezer_API_2
import JTM_10_fuzzywuzzy_match_4
import JTM_11_fuzzywuzzy_match_5
import JTM_12_fuzzywuzzy_match_6
import JTM_13_fuzzywuzzy_match_7


def main():
    # start time of function
    start_time = time.time()

    print('JTM_06_lastfm_API')
    JTM_06_lastfm_API.main()
    print('JTM_07_fuzzywuzzy_match_2')
    JTM_07_fuzzywuzzy_match_2.main()
    print('JTM_08_fuzzywuzzy_match_3')
    JTM_08_fuzzywuzzy_match_3.main()
    print('JTM_09_deezer_API_2')
    JTM_09_deezer_API_2.main()
    print('JTM_10_fuzzywuzzy_match_4')
    JTM_10_fuzzywuzzy_match_4.main()
    print('JTM_11_fuzzywuzzy_match_5')
    JTM_11_fuzzywuzzy_match_5.main()
    print('JTM_12_fuzzywuzzy_match_6')
    JTM_12_fuzzywuzzy_match_6.main()
    print('JTM_13_fuzzywuzzy_match_6')
    JTM_13_fuzzywuzzy_match_7.main()

    # end time of program + duration
    end_time = time.time()
    print('\n', int(end_time - start_time), 'sec\n')

if __name__ == "__main__":
    main()