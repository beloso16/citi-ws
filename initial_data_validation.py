
# Example usage
import ws_functions
import pandas as pd

# Combining the ELLT FILES
ellt_path = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/raw_ellt_files'
lld_path = '/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/raw_lld_files'

#check for weird column names
outlier_ellt_column_df = ws_functions.get_unique_column_files(ellt_path)
outlier_lld_column_df = ws_functions.get_unique_column_files(lld_path)

final_ellt_df = ()
final_lld_df = ()

if outlier_ellt_column_df.empty and outlier_lld_column_df.empty:
    #combine all into a single df if no outliers

    final_ellt_df = ws_functions.combine_all_files(ellt_path)
    #drop duplicates
    print(final_ellt_df)
    final_ellt_df = final_ellt_df.drop_duplicates()
    print(final_ellt_df)

    final_lld_df = ws_functions.combine_all_files(lld_path, add_month_year=True)
    print(final_lld_df)

    #change the format of the dates
    
    # Convert date columns to string
    date_columns = ['First Payment Date', 'Maturity Date', 'Interest Only Expiration Date',
                    'Next Interest Rate Change Date', 'Next Payment Change Date',
                    'First Rate Change Date', 'Interest Rate at Next Reset Date',
                    'Origination Date', 'BPO Date', 'Scheduled Balance Paid Thru Date',
                    'First Payment Change Date']

    final_lld_df[date_columns] = final_lld_df[date_columns].astype(str)

    for column in date_columns:
        final_lld_df[column] = final_lld_df[column].apply(
            lambda x: '2' + str(int(x)).zfill(7) if pd.notna(x) and pd.to_numeric(x, errors='coerce') == x else '' if pd.isna(x) else x
    )
    
    #drop duplicates
    final_lld_df = final_lld_df.drop_duplicates()
    final_lld_df.replace('nan', '', inplace=True)
    print(final_lld_df)

    #move deal id
    column_order = ['Deal ID'] + [col for col in final_lld_df if col != 'Deal ID']
    final_lld_df = final_lld_df[column_order]

    print(final_ellt_df)
    print(final_lld_df)
    #finally save everything
    final_ellt_df.to_csv('/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/final_ellt_df.csv', index=False)
    final_lld_df.to_csv('/Users/faustine/Desktop/trex_tech_exam/citi-ws/downloaded_files/final_lld_df.csv', index=False)

else:
#investigate
    print("Did not meet criteria")


    """
    #check if all investor loan numbers are in lld | should be empty
    investor_loan_numbers_ellt = final_ellt_df['Investor Loan #']
    result_df = final_ellt_df[~investor_loan_numbers_ellt.isin(final_lld_df['Loan Identification Number'])]
    #print(result_df)

    #assume these columns are not nullable for ellt, should be no empty
    ellt_columns_to_check = ['Transaction ID', 'Investor Loan #', 'Distribution Date', 'Paid To Date']
    empty_ellt_rows = final_ellt_df[final_ellt_df[ellt_columns_to_check].isnull().any(axis=1) | (final_ellt_df[ellt_columns_to_check] == '')]
    #print(empty_ellt_rows)

    #assume these columns are not nullable for lld, should be no empty
    lld_columns_to_check = ['Loan Identification Number']
    empty_lld_rows = final_lld_df[final_lld_df[lld_columns_to_check].isnull().any(axis=1) | (final_lld_df[lld_columns_to_check] == '')]
    #print(empty_lld_rows)

    """