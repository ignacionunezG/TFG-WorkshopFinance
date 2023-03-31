# -*- coding: utf-8 -*-
"""find_company.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q0CsBkzKp9HVtrhh1PD1WO7vstlFbuCF
"""

import pprint
import requests

def search_ticker(input):
  url1 = "https://cloud.iexapis.com/stable/search/" + input + "?token=pk_b684e0058b244ac7bd8b6d92284af164"
  temp1 = requests.get(url1)
  op1 = temp1.json()
  res1 = [ (sub['symbol'], sub['name']) for sub in op1 ]
  return res1

def search_company(input):
  url2 = "https://api-v2.intrinio.com/companies/search?query=Appl&api_key=OjAwYjk1OWYxZGEzYWQ2Y2VjN2YyMWExY2RkMTM2Y2Uz"
  temp2 = requests.get(url2)
  op2 = temp2.json()
  op2 = op2['companies']
  res2 = [ (sub['ticker'], sub['name']) for sub in op2 ]
  # replace the None type with empty string. 
  res2 = [("",y) if x == None else (x,y) for (x,y) in res2]
  return res2

def find_company_name(input):
  res_company = []
  res_ticker = []
  try: 
    res_company = search_company(input)
  except (RuntimeError, TypeError, NameError):
    pass
  try: 
    res_ticker = search_ticker(input)
  except (RuntimeError, TypeError, NameError):
    pass  
  res_ticker = sorted(res_ticker)
  res_company.sort(key=lambda x:x[1])
  res = res_company+res_ticker
  res_final = list(set(res))
  return res_final

out = find_company_name("tesla")
print(out)