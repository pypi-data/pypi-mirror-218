import pandas as pd
import numpy as np
from scipy.stats import *

def LoadFromCSV(CSVPath):
  return pd.read_csv(CSVPath)

def LoadFromDict(dictData):
  return pd.DataFrame(dictData)

def LoadFromExcel(ExcelPath):
    return pd.read_csv(ExcelPath)

""" Independent T-Test
Parameters (Input):
==================================================
df        : Pandas DataFrame 2xN (Two Columns x N Row)

variable1*: string
                Independent variable (X)
                Name of DataFrame column object

variable2*: string
                Dependent variable (Y)
                Name of DataFrame column object

*: Required Parameter

Return (Output):
===================================================
Type: dictionary
Description: T-Test Stats
"""
def IndTTest(df,variable1,variable2):

  if df is None:
    raise Exception("No data loaded")

  if len(df[variable1].value_counts().index)>2:
    raise Exception("The number of groups cannot be greater than 2")

  # Create a dictionary object for the store data and etc.
  dataCollection=dict()

  # Extract the groups from DataFrame and put into the dataCollection dictionary object
  for idx in df[variable1].value_counts().index:
    dataCollection[idx]={"data":df.query(variable1 + "==" + str(idx))[variable2]}

  # Extract the raw data from dictionary object to pass scipy.stats functions
  rawData=list()
  for item in dataCollection:
    rawData.append(dataCollection[item]["data"])

  data1,data2=rawData[0],rawData[1]

  # Calculate Indepentend T-Test
  result1 = ttest_ind(data1, data2)

  # Calculate Levent Test
  result2=levene(data1, data2,center='mean')

  # Calculate Indepentend Welch Test
  result3= ttest_ind(data1, data2,equal_var = False)

  # Calculate Degree of Freedom score
  dofF=len(data1)+len(data2)-2

  # Calculate group descriptive statistics
  groupStats=list()
  for item in dataCollection:
    group=dict()
    group[item]={"N":dataCollection[item]["data"].count(),
                   "Mean":dataCollection[item]["data"].mean(),
                   "StdDev":dataCollection[item]["data"].std()
    }
    groupStats.append(group)

  # Create  dictionary object(dictReturn) to return stats
  dictReturn={
        # Groups statistics
        "groupStats":groupStats,

        # T-Test results
        "TTest":{
            "t":result1[0],
            "df":dofF,
            "sigTwoTailed":result1[1]
        },

        # Levene test results
        "LeveneTest":
        {
         "F":result2[0],
         "sigTwoTailed":result2[1]

        },

        # Welch test results
        "WelchTest":{
            "t":result3[0],
            "sigTwoTailed":result3[1]
        }
  }

  return dictReturn