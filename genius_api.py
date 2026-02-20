
import requests
import os
from multiprocessing import Pool
from time import sleep

# user-installed
import pandas as pd
from tqdm import tqdm
from numpy.random import uniform
from dotenv import load_dotenv

load_dotenv()


ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
NAME_DEMO = __name__

def genius(search_term, per_page=15):
    
    genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                        f"access_token={ACCESS_TOKEN}&per_page={per_page}"
    
    response = requests.get(genius_search_url)
    json_data = response.json()
    
    return json_data['response']['hits']

def genius_to_df(search_term, n_results_per_term=10, 
                 verbose=True, savepath=None):
   
    json_data = genius(search_term, per_page=n_results_per_term)
    hits = [hit['result'] for hit in json_data]
    df = pd.DataFrame(hits)

    # expand dictionary elements
    df_stats = df['stats'].apply(pd.Series)
    df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                    inplace=True)
    
    df_primary = df['primary_artist'].apply(pd.Series)
    df_primary.rename(columns={c:'primary_artist_' + c 
                               for c in df_primary.columns},
                      inplace=True)
    
    df = pd.concat((df, df_stats, df_primary), axis=1)
    
    if verbose:
        print(f'PID: {os.getpid()} ... search_term:', search_term)
        print(f"Data gathered for {search_term}.")

  
    if savepath:
        df.to_csv(savepath + '/genius-{searchname}.csv', 
                  index=False)

    return df

def genius_to_dfs(search_terms, **kwargs):
  
    dfs = []

   
    for search_term in tqdm(search_terms):
        df = genius_to_df(search_term, **kwargs)
        
       
        dfs.append(df)

    return pd.concat(dfs)

def testing():
    print('Testing 1, 2, 3 ...')
    return None

def job_test(num, mult=2):
    print(f'PID: {os.getpid()} ... num:', num)
    sleep(uniform(0.5, 1.5))
    return num * mult



if __name__ == "__main__":

 
    testing()

   
