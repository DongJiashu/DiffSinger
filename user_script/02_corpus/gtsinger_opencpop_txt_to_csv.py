#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import codecs


# In[11]:


transcriptions = []
with codecs.open('/path/to/your/transcriptions.txt', 'r', 'utf-8') as f:
    for l in f:
        tmp = l.strip().split('|')
        ph_seq = tmp[2].strip().split()
        ph_dur = list(map(float, tmp[5].strip().split()))
        ph_seq = ' '.join(ph_seq)
        ph_dur = ' '.join([str(round(d, 6)) for d in ph_dur])
        transcriptions.append({'name': tmp[0], 'ph_seq': ph_seq, 'ph_dur': ph_dur})


# In[12]:


with open('/path/to/your/transcriptions.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'ph_seq', 'ph_dur'])
    writer.writeheader()
    writer.writerows(transcriptions)


# In[ ]:




