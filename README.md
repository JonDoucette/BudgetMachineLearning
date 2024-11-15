# BudgetMachineLearning
This is a tool that takes the outputs from our credit providers and uses machine learning to help categorize and label the purchases with categories and vendors.

# The Why
Each month, my wife and I download all of our bank activity statements to monitor purchases for our budget. These files are all formatted differently and need to be combined into one common file. We then have to go and provide a Vendor and Category for each purchase. I figured that I could train a model that goes off our previous data to help reduce the time spent on this process. 

# Results
This process used to take us around 30 minutes each month, but with this script it has reduced it to about 5 minutes (which consists of filling in the categories and vendors that the model isn't sure of). 

# Code Explanation
We will first start with the `budgetLearn.py` or the `budgetLearnWithAmount.py` files. These will take a provided Excel file that has the columns: Date, Description, Amount, Vendor, and Category. The script will then split up the data into training and testing data and run a Random Forest Classifier on it. The program will print out the confidence score for both the Vendor and the Category fields. I would recommend running both python files on your dataset and finding out which one has the higher confidence. In my case it was the `budgetLearn.py` with accuracies of:

- Vendor Accuracy: 78.16%
- Category Accuracy: 82.63%

Moving on to the `rawDataFormatting.py` file. This file will check my network drive (E:\) for the bank statement files. Each file has specific naming conventions based on the account that the file is retrieved from. The script will look for specific naming conventions in determining which file belongs to which bank. It will then do the data formatting on all files and combine them into one spreadsheet.

With that combined spreadsheet, we move on to `budgetApply.py`. This script will take the combined spreadsheet and apply the trained model from the first steps to this spreadsheet returning a spreadsheet formatted correctly with two additional columns called:

- Predicted_Vendor
- Predicted_Category
