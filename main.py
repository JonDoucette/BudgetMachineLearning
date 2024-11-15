from Helpers.rawDataFormatting import formatRawData
from Helpers.budgetApply import add_predictions_to_excel
from Helpers.budgetLearn import train_model
import pandas as pd

def main():
    formatRawData('formattedData.xlsx')
    add_predictions_to_excel('formattedData.xlsx', 'results.xlsx')

def trainModel():
    data = pd.read_excel('Final - Complete Budget & Receipt Tracker.xlsx')
    train_model(data)

if __name__ == "__main__":
    main()