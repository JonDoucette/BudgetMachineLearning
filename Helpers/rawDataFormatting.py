import pandas as pd
import os

def formatChase(chase_data_location):
    print('Formatting Chase')
    chase_data = pd.read_csv(chase_data_location)

    # Remove any payments of the card
    chase_data = chase_data[chase_data['Type'] != 'Payment']

    chase_data = chase_data.rename(columns={
        'Transaction Date': 'Date',
    })
    chase_data['Card'] = "Jon's Chase"
    chase_data = chase_data[['Date', 'Description', 'Amount', 'Card']]
    return chase_data

def formatFargo(fargo_data_location):
    print('Formatting Wells Fargo...')
    column_names = ['Date', 'Amount', 'Star', 'Empty', 'Description']
    wells_fargo_data = pd.read_csv(fargo_data_location, header=None, names=column_names)
    wells_fargo_data['Card'] = "Jon's Wells Fargo"
    # Remove rows where 'Description' starts with 'Chase Credit'
    wells_fargo_data = wells_fargo_data[~wells_fargo_data['Description'].str.startswith('CHASE CREDIT CRD EPAY', na=False)]
    wells_fargo_data = wells_fargo_data[['Date', 'Description', 'Amount', 'Card']]
    return wells_fargo_data

def formatNsb(nsb_data_location):
    print('Formatting NSB...')
    column_names = ['Date', 'Account', 'Description', 'Check#', 'DepositSlip', 'Memo', 'TransactionCode', 'Credit', 'Debit']
    nsb_data = pd.read_csv(nsb_data_location, header=None, names=column_names)
    #Remove first 3 rows
    nsb_data = nsb_data.iloc[3:]
    nsb_data['Card'] = "Kelsey's NSB"
    nsb_data['Amount'] = nsb_data['Credit'].fillna(0).astype(float) + nsb_data['Debit'].fillna(0).astype(float)
    # Remove rows where 'Description' starts with 'Chase Credit'
    nsb_data = nsb_data[~nsb_data['Description'].str.startswith('DISCOVER         E-PAYMENT', na=False)]
    nsb_data = nsb_data[['Date', 'Description', 'Amount', 'Card']]
    return nsb_data

def formatDiscover(discover_data_location):
    print('Formatting Discover...')
    discover_data = pd.read_csv(discover_data_location)
    discover_data = discover_data.rename(columns={
        'Trans. Date': 'Date',
    })
    discover_data['Card'] = "Kelsey's Discover"
    discover_data['Amount'] = discover_data['Amount'].astype(float) * -1.0

    # Remove rows where 'Description' starts with 'Chase Credit'
    discover_data = discover_data[~discover_data['Description'].str.startswith('INTERNET PAYMENT - THANK YOU', na=False)]
    discover_data = discover_data[['Date', 'Description', 'Amount', 'Card']]
    return discover_data

def findFileLocations():
    #Look at E Drive
    docs = os.listdir("E:\\")
    docs = [doc for doc in docs if doc.lower().endswith('.xlsx') or doc.lower().endswith('.csv')]
    docs = [os.path.join("E:\\", doc) for doc in docs]

    chase_location = findSpecificFile(docs, 'Chase2032')
    fargo_location = findSpecificFile(docs, 'Checking1')
    nsb_location = findSpecificFile(docs, 'Transactions')
    discover_location = findSpecificFile(docs, 'Discover-Statement', True)

    return chase_location, fargo_location, nsb_location, discover_location

def findSpecificFile(docs, fileStarts, multiple = False):
    location = [doc for doc in docs if doc[3:].startswith(fileStarts)]
    if len(location) == 0:
        location = None
    elif not multiple:
        location = location[0]

    return location

def formatRawData(outputFileName):
    chase_location, fargo_location, nsb_location, discover_location = findFileLocations()

    #Get Data
    chase_data = formatChase(chase_location)
    wells_fargo_data = formatFargo(fargo_location)
    nsb_data = formatNsb(nsb_location)
    discover_data = pd.DataFrame()
    for discover_file in discover_location:
        discover_data = pd.concat([discover_data, formatDiscover(discover_file)])

    # Save the result to an Excel file
    combined_df = pd.concat([chase_data, wells_fargo_data, nsb_data, discover_data], ignore_index=True)

    #Add additional empty columns to make formatting easier for Budget Input
    combined_df['Empty'] = None
    combined_df['Empty2'] = None
    combined_df['Empty3'] = None

    combined_df.to_excel(outputFileName, index=False)
