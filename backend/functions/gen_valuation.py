import pandas as pd
import requests
from time import time
from datetime import datetime
import random
import time

#FROM EACH COMP, WE NEED (priority 1):
#enterprise value
#evToRevenueLTM
#evToEbitdaLTM

####FUNCTIONS THAT WE WILL NEED

#get_metrics:Gets financial metrics from the comps and the target from IEX
#add_COMP:Adds comparables to COMPS table from IEX
#add_VALUATION:Adds new valuation to VALUATION table from IEX. This only contains the default values
#update_VALUATION: As soon as a new comp is added to the valuation, a valuation is generated and the valuation already added to the table is updated
#get_output:Gets valuation output
#generate_valuation:Generates Valuation. Main function to call

def get_metrics(company,comp_tgt,iex_api_key):
    #Preparing code
    fundamentals = [] #Fundamentals will store desired financial metrics of each company

    ##Fetching API
    #fundamentals_api obtains ebitda and revenue
    #both if we are dealing with the comp or with a tgt, we want the ebitdaLTM and the revenueLTM
    fundamentals_api="https://cloud.iexapis.com/stable/time-series/fundamentals/"+company+"/ttm?token="+iex_api_key
    fundamentals_request=requests.get(fundamentals_api)
    ebitdaLTM = fundamentals_request.json()[0]['ebitdaReported']
    revenueLTM= fundamentals_request.json()[0]['revenue']

    
    if comp_tgt=="comp":
        #fundamental_valuations_api obtains enterpriseValue. Only when we are fetching a comp we are interested in enterpriseValue.
        
        ev_api = "https://cloud.iexapis.com/v1/stock/"+company+"/advanced-stats?token="+iex_api_key
        ev_request=requests.get(ev_api)
        enterpriseValue = ev_request.json()['enterpriseValue']

        #calculating evToEbitdaLTM
        evToEbitdaLTM=enterpriseValue/ebitdaLTM
        #adding evToEbitda to fundamentals
        fundamentals.append(evToEbitdaLTM)
    
        #calculating evToRevenueLTM
        evToRevenueLTM=enterpriseValue/revenueLTM
        #adding evToRevenue to fundamentals
        fundamentals.append(evToRevenueLTM)
        
        #if company is a comp: fundamentals=[evToEbitdaLTM,evToRevenueLTM]
    else:
        
        fundamentals.append(ebitdaLTM)
        fundamentals.append(revenueLTM)
        
        #if company is a tgt: fundamentals=[ebitdaLTM, revenueLTM]

    return fundamentals

def add_COMP(compSymbol,valuationId,iex_api_key):
    fundamentals=get_metrics(compSymbol,"comp", iex_api_key)
    evToEbitdaLTM=fundamentals[0]
    evToRevenueLTM=fundamentals[1]

    #If this dataset COMPS is empty, the firs compId will be 1. From then on, each compId will be the previous compId+1.
    url = "https://workshopfinance.iex.cloud/v1/data/workshopfinance/COMPS?&token="+iex_api_key
    comps=[{        
        "compSymbol": compSymbol,
        "evToEbitdaLTM": evToEbitdaLTM,
        "evToRevenueLTM": evToRevenueLTM,
        "valuationId": valuationId
    }]

    #POST each comp into the COMPS dataset
    r = requests.post(url, json=comps)
    if r.status_code==200:
        return "Successful Comps Post"
    else:
        return "Unsuccessful Comps Post"

def update_VALUATION(footballFieldId, multiples,ev,valuationTimeSeries,iex_api_key):
    url = "https://workshopfinance.iex.cloud/v1/data/workshopfinance/VALUATIONS/"+footballFieldId+"/"+valuationTimeSeries+"/?&token="+iex_api_key
    print(url)
    valuation=requests.get(url).json()
    print("valuation0")
    print(valuation)
    #Depending on the desired stat, we will want one row of multiples/ev or another.
    #However, even though the stat is changed, no recalculations should be made. All possible calculation should already be made
    #If Output=Mult:
    valuation[0]["valuationMultAvEvEbitdaLTM"]=multiples.iloc[0]['evToEbitdaLTM'] #Stat=Av, Multiple=evToEbitdaLTM
    valuation[0]["valuationMultMedEvEbitdaLTM"]=multiples.iloc[1]['evToEbitdaLTM'] #Stat=Median, Multiple=evToEbitdaLTM
    valuation[0]["valuationMultHighEvEbitdaLTM"]=multiples.iloc[2]['evToEbitdaLTM']#Stat=High, Multiple=evToEbitdaLTM
    valuation[0]["valuationMultLowEvEbitdaLTM"]=multiples.iloc[3]['evToEbitdaLTM']#Stat=Low, Multiple=evToEbitdaLTM
    valuation[0]["valuationMultAvEvRevLTM"]=multiples.iloc[0]['evToRevenueLTM']#Stat=Av, Multiple=evToRevLTM
    valuation[0]["valuationMultMedEvRevLTM"]=multiples.iloc[1]['evToRevenueLTM']#Stat=Median, Multiple=evToRevLTM
    valuation[0]["valuationMultHighEvRevLTM"]=multiples.iloc[2]['evToRevenueLTM']#Stat=High, Multiple=evToRevLTM
    valuation[0]["valuationMultLowEvRevLTM"]=multiples.iloc[3]['evToRevenueLTM']#Stat=Low, Multiple=evToRevLTM
    #If Output=Ev:
    valuation[0]["valuationEvAvEvEbitdaLTM"]=ev.iloc[0]['evToEbitdaLTM']#Stat=Av, Multiple=evToEbitdaLTM
    valuation[0]["valuationEvMedEvEbitdaLTM"]=ev.iloc[1]['evToEbitdaLTM']#Stat=Median, Multiple=evToEbitdaLTM
    valuation[0]["valuationEvHighEvEbitdaLTM"]=ev.iloc[2]['evToEbitdaLTM']#Stat=High, Multiple=evToEbitdaLTM
    valuation[0]["valuationEvLowEvEbitdaLTM"]=ev.iloc[3]['evToEbitdaLTM']#Stat=Low, Multiple=evToEbitdaLTM
    valuation[0]["valuationEvAvEvRevLTM"]=ev.iloc[0]['evToRevenueLTM']#Stat=Av, Multiple=evToRevLTM
    valuation[0]["valuationEvMedEvRevLTM"]=ev.iloc[1]['evToRevenueLTM']#Stat=Median, Multiple=evToRevLTM
    valuation[0]["valuationEvHighEvRevLTM"]=ev.iloc[2]['evToRevenueLTM']#Stat=High, Multiple=evToRevLTM
    valuation[0]["valuationEvLowEvRevLTM"]=ev.iloc[3]['evToRevenueLTM']#Stat=Low, Multiple=evToRevLTM
    
    #valuationCompsDate:
    #valuation[0]['valuationCompsDate']=valuationCompsDate
    print("valuation")
    print(valuation)
   
    url="https://cloud.iexapis.com/v1/record/workshopfinance/VALUATIONS?duplicateKeyHandling=true&wait=true&token="+iex_api_key
    #url="https://workspace.iex.cloud/v1/datasets/workshopfinance/VALUATIONS?token=sk_cd4257e5aa684ab6a245c13b45f0e204"
    r=requests.post(url, json=valuation)
    print(r)
    return r
    



def get_output(basket_of_comps, valuationId, targetSymbol, desired_multiples, iex_api_key):

    comps_raw_data = []
    tgt_raw_data=[]
    
    #We obtain evToEbitdaLTM and evToRevenueLTM for the comps

    for comp in basket_of_comps:
        url="https://workshopfinance.iex.cloud/v1/data/workshopfinance/COMPS/"+valuationId+"/"+comp+"?token="+iex_api_key
        r=requests.get(url).json()

        evToEbitdaLTM=r[0]['evToEbitdaLTM']
        evToRevenueLTM=r[0]['evToRevenueLTM']
        comps_raw_data.append([evToEbitdaLTM,evToRevenueLTM])
        

    #We obtain ebitdaLTM and revenueLTM for the tgt
    tgt_raw_data.append(get_metrics(targetSymbol,"tgt",iex_api_key))
  
    #Specify the columns for the tgt dataframe (ebitdaLTM and revenueLTM)
    
    desired_metrics=desired_multiples[:]
    for i in range(0,len(desired_metrics)):
        desired_metrics[i]=desired_metrics[i][4].lower()+desired_metrics[i][5:]
   
    #We will have 2 dataframes: comps_df and tgt_df.
    #comps_df will be a datafarme containing the raw_data(ev, evToEbitda, evToRevenue)
    #tgt_df will be a dataframe containing the raw_data(ebitda, revenue) of the tgt 
    
    comps_df = pd.DataFrame(comps_raw_data, columns = desired_multiples, index = basket_of_comps)
    tgt_df = pd.DataFrame(tgt_raw_data, columns = desired_metrics, index=[targetSymbol])
    
    #multiples contains the avg, median, high and low output for each multiple
    #ev contains the av, median, high and low ev of the target
    multiples = pd.DataFrame(columns = desired_multiples, index = ['Avg', 'Median', 'High' ,'Low'])
    ev=pd.DataFrame(columns = desired_multiples, index = ['Avg', 'Median', 'High' ,'Low'])

    multiples.iloc[0] = comps_df.mean() #Comp avg ev, evToEbitda, evToRevenue
    multiples.iloc[1] = comps_df.median()#Comp median ev, evToEbitda, evToRevenue
    multiples.iloc[2] = comps_df.max()#Comp max ev, evToEbitda, evToRevenue
    multiples.iloc[3] = comps_df.min()#Comps min ev, evToEbitda, evToRevenue
    print(multiples)
    #ev is multiples*ebitda or revenue    
    ev['evToEbitdaLTM']=multiples['evToEbitdaLTM']*float(tgt_df['ebitdaLTM'])
    ev['evToRevenueLTM']=multiples['evToRevenueLTM']*float(tgt_df['revenueLTM'])
    

    output=[multiples,ev]
    
    #We add comps to our comps table. Let's re-think this in the future.
    #for i in range(0,len(comps_df.index)):
    #    add_COMP(comps_df.index[i], comps_df.iloc[i]['evToEbitdaLTM'], comps_df.iloc[i]['evToRevenueLTM'],valuationId,iex_api_key)
    return output


####WE MIGHT NOT NEED THIS FUNCTION
#def retrieveTgt(userId, targetSymbol, iex_api_key):
#    url = "https://workshopfinance.iex.cloud/v1/data/workshopfinance/TARGETS/"+userId+"/"+targetSymbol+"&token="+iex_api_key
#    r=requests.get(url).json()
#    tgt=r[0]['targetSymbol']
#    return tgt
###


def retrieve_valuation_comps(valuationId, iex_api_key):
    #How to obtain all queries from API
    basket_of_comps=[]
    while basket_of_comps==[]:
        url = "https://workshopfinance.iex.cloud/v1/data/workshopfinance/COMPS/"+valuationId+"/?last=100&token="+iex_api_key
        print("url")
        print(url)
        print("aqui")
        r=requests.get(url).json()
        print(r)
        for comp in r:
            print(comp)
            basket_of_comps.append(comp['compSymbol'])

    print("boc")
    print(basket_of_comps)
    return basket_of_comps

def generate_valuation(targetId, targetSymbol, desired_multiples, valuationTimeSeries, iex_api_key, footballFieldTimeSeries):
    #We preprare the IDs:
    footballFieldId=targetId+"-"+footballFieldTimeSeries
    valuationId=footballFieldId+"-"+valuationTimeSeries


    #AT THIS MOMENT, WE HAVE TO DO THIS, LATER WE WILL DELETE THE FOLLOWING 5 LINES OF CODE INVOLVING ADD_COMP:
    #comps = ["KO", "TSLA", 'NKE', 'DIS', "MA", "PG", "GOOGL", "AMZN", "MRK", "JNJ", "META"]

    #basket_of_comps = random.sample(comps, 2)
    #for comp in basket_of_comps:
    #   add_COMP(comp,valuationId,valuationCompsDate,iex_api_key)
    #time.sleep(0.1)

    #We get the basket of comps:
    basket_of_comps=retrieve_valuation_comps(valuationId, iex_api_key)
    print (basket_of_comps)
    output=get_output(basket_of_comps, valuationId, targetSymbol, desired_multiples,iex_api_key)
    multiples=output[0]
    ev=output[1]
    
    
    update_VALUATION(footballFieldId, multiples, ev,valuationTimeSeries,iex_api_key)

def add_VALUATION(footballFieldId, iex_api_key, valuationTimeSeries):
    now = datetime.now()
    #timeDateCreated = now.strftime("%m/%d/%Y %H:%M:%S")# timeDateCreated value has to be fixed, can not be editted. It contains the
    #timeDateCreated = timeDateCreated[:6]+timeDateCreated[8:-3] #time and date of when the valuation was generated for the first time
    #valuationCompsDate=now.strftime("%m/%d/%Y")
    valuationType="COMPS"
    
    url_valuation_name="https://workshopfinance.iex.cloud/v1/data/workshopfinance/VALUATIONS/"+footballFieldId+"/?last=100&token="+iex_api_key
    resp = requests.get(url_valuation_name).json()
    valuationName="VALUATION "+str(len(resp)+1)
    #After prototype session, discomment this:
    #valuationTimeSeries=str(int(time()*1000000))
    url = "https://workshopfinance.iex.cloud/v1/data/workshopfinance/VALUATIONS?&token="+iex_api_key
    valuation=[
    {
        
        "footballFieldId":footballFieldId,
        "valuationName":valuationName,
        "valuationTimeSeries":valuationTimeSeries,
        "valuationType":valuationType

    }]

    #POST into the VALUATIONS dataset
    r = requests.post(url, json=valuation)

    return r

def update_VALUATION_NAME(targetId,footballFieldTimeSeries,valuationTimeSeries,valuationName,iex_api_key):
    
    footballFieldId=targetId+footballFieldTimeSeries

    url="https://workshopfinance.iex.cloud/v1/data/workshopfinance/VALUATIONS/"+footballFieldId+"/"+valuationTimeSeries+"?token="+iex_api_key
    valuation=requests.get(url).json()
    valuation[0]['valuationName']=valuationName

    #url="https://workshopfinance.iex.cloud/v1/data/workshopfinance/VALUATIONS?&token="+iex_api_key
    url="https://cloud.iexapis.com/v1/record/workshopfinance/VALUATIONS?duplicateKeyHandling=true&wait=true&token="+iex_api_key
    r=requests.post(url, json=valuation)
    return r


