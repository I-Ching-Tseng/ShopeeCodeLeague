#!/usr/bin/env python
# coding: utf-8
!unzip students-2-shopee-code-league-order-brushing.zip
# In[1]:


import pandas as pd
import numpy as np
from tqdm import tqdm


# In[2]:


df_all = pd.read_csv('order_brush_order.csv')


# In[3]:


df_all


# In[4]:


df_shop = df_all.groupby('shopid')


# In[5]:


res = {shopid:[] for shopid in df_all['shopid'].unique()}


# In[6]:


from datetime import timedelta


# In[7]:


for shopid in tqdm(res):
    #if not shopid == 175531295: continue
    df = df_shop.get_group(shopid)
    #print(shopid)
    #print(len(df))
    if len(df) < 3:
        res[shopid] = '0'
    else:
        df = df.sort_values('event_time')
        #print(df)
        order_brush_dict = {}
        userid, event_time = df['userid'], df['event_time']
        event_time = pd.to_datetime(event_time)
        end_time = event_time+timedelta(hours=1)
        for u, s, e in zip(userid, event_time, end_time):
            index = (event_time <= e) & (event_time >= s)
            
            n_order = np.sum(index)

            unique_user = userid[index].unique()
            rate = n_order / len(unique_user)
            
            if rate >= 3:
                for _userid, _time in zip(userid[index], event_time[index]):
                    key_u = str(_userid)
                    if not key_u in order_brush_dict:
                        order_brush_dict[key_u] = set()
                    val_t = str(_time)
                    order_brush_dict[key_u].add(val_t)
            
        
        if len(order_brush_dict) == 0:
            res[shopid] = '0'
        else:

            max_n_order = 0
            max_n_users = ''
            for u in order_brush_dict:
                if len(order_brush_dict[u]) > max_n_order:
                    max_n_users = str(u)          
                    max_n_order = len(order_brush_dict[u])
                elif len(order_brush_dict[u]) == max_n_order:
                    max_n_users = f'{max_n_users}&{u}'
            res[shopid] = max_n_users
    #print(shopid, ':', res[shopid])


# In[9]:


f = open('output', 'w')
print('shopid,userid', file=f)
for shopid in tqdm(res):
    print(f'{shopid},{res[shopid]}', file=f)
    if '&' in res[shopid]:
        print(f'shopid:{shopid}, res:{res[shopid]}')


# In[ ]:




