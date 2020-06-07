#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib
import requests
from bs4 import BeautifulSoup
import tldextract
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
# desktop user-agent
import re
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
import pandas as pd
import numpy as np
import streamlit as st

import time
# In[62]:


tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = set(stopwords.words('english'))
ps = PorterStemmer()


# In[60]:


en_stopwords.remove('how')
en_stopwords.remove('why')
en_stopwords.remove('what')
en_stopwords.remove('when')


# In[74]:
st.title("Meta Title Builder On Frameworks")
st.text("--------------------------------------------")
st.text("What & Why: A script to scrape the titles & descriptions of the top 10 ranking URLS on Google for the entered query.")
st.text("Based on the scraped data, we generate a word & frequency data table.")
st.text("We use this data along with two frameworks (shared by popular SEO publishers)")
st.text("The goal is to create more compelling Meta Titles to improve CTR")
st.text("At VWO.com, we have followed this framwork for our blog posts, & we have seen positive results in CTR.")
st.text("Please do give these blog posts a read before using the tool.")
st.text("Link for Framework 1: https://searchengineland.com/5-brilliant-headline-hacks-crazy-high-organic-click-rates-249320")
st.text("Link for Framework 2: https://www.wordstream.com/blog/ws/2017/02/21/features-vs-benefits")
st.text("--------------------------------------------")


st.title("How to Use This Tool?")
st.text("Watch this video:                                               . Or follow the steps.")
st.text("Step 1: Enter your focus keyword")
st.text("Step 2: Select the Google version for your target country")
st.text("Wait for results to be scraped")
st.text("--------------------------------------------")
st.text("--------------------------------------------")

df=pd.read_csv(r"countries.csv")
countries=np.array(df)
countries=dict(countries)
#s_name=st.selectbox('Country',('Andorra', 'United Arab Emirates', 'Afghanistan', 'Antigua and Barbuda', 'Anguilla', 'Albania', 'Armenia', 'Angola', 'Argentina', 'American Samoa', 'Austria', 'Australia', 'Azerbaijan', 'Bosnia and Herzegovina', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi', 'Benin', 'Brunei', 'Bolivia', 'Brazil', 'Bahamas', 'Bhutan', 'Botswana', 'Belarus', 'Belize', 'Canada', 'Cambodia', 'Cocos (Keeling) Islands', 'Democratic Republic of the Congo', 'Central African Republic', 'Catalan Countries', 'Republic of the Congo', 'Switzerland', 'Ivory Coast', 'Cook Islands', 'Chile', 'Cameroon', 'China', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Cyprus', 'Czech Republic', 'Germany', 'Djibouti', 'Denmark', 'Dominica', 'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Spain', 'Ethiopia', 'Finland', 'Fiji', 'Federated States of Micronesia', 'France', 'Gabon', 'Georgia','French Guiana', 'Guernsey', 'Ghana', 'Gibraltar', 'Greenland', 'Gambia', 'Guadeloupe', 'Greece', 'Guatemala', 'Guyana', 'Hong Kong', 'Honduras', 'Croatia', 'Haiti', 'Hungary', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Isle of Man', 'India', 'British Indian Ocean Territory', 'Iceland', 'Italy', 'Jersey', 'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kiribati', 'Kyrgyzstan', 'South Korea', 'Kuwait', 'Kazakhstan', 'Laos', 'Lebanon', 'Saint Lucia', 'Liechtenstein', 'Sri Lanka', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco', 'Moldova', 'Montenegro', 'Madagascar', 'Macedonia', 'Mali', 'Myanmar', 'Mongolia', 'Montserrat', 'Malta', 'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia', 'Mozambique', 'Namibia', 'Niger', 'Norfolk Island', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'Nauru', 'Niue', 'New Zealand', 'Oman', 'Pakistan', 'Panama', 'Peru', 'Philippines', 'Poland', 'Papua New Guinea', 'Pitcairn Islands', 'Puerto Rico', 'Palestine[4]', 'Portugal', 'Paraguay', 'Qatar', 'Romania', 'Serbia', 'Russia', 'Rwanda', 'Saudi Arabia', 'Solomon Islands', 'Seychelles', 'Sweden', 'Singapore', 'Saint Helena, Ascension and Tristan da Cunha', 'Slovenia', 'Slovakia', 'Sierra Leone', 'Senegal', 'San Marino', 'Somalia', 'SÃ£o TomÃ© and PrÃ­ncipe', 'Suriname', 'El Salvador', 'Chad', 'Togo', 'Thailand', 'Tajikistan', 'Tokelau', 'Timor-Leste', 'Turkmenistan', 'Tonga', 'Tunisia', 'Turkey', 'Trinidad and Tobago', 'Taiwan', 'Tanzania', 'Ukraine', 'Uganda', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Saint Vincent and the Grenadines', 'Venezuela', 'British Virgin Islands', 'United States Virgin Islands', 'Vietnam', 'Vanuatu', 'Samoa', 'South Africa', 'Zambia', 'Zimbabwe'))
c_name=st.selectbox('Country',('Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Ascension Island', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Basque Country', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bonaire', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burma', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde (in Portuguese: Cabo Verde)', 'Catalonia', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos ', 'Colombia', 'Comoros', 'Congo', 'Congo', 'Cook Islands', 'Costa Rica', 'CÃ´te dâ€™Ivoire', 'Croatia', 'Cuba', 'CuraÃ§ao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'East Timor', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'European Union', 'Falkland Islands', 'Faeroe Islands', 'Federated States of Micronesia', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern and Antarctic Lands', 'Gabon', 'Galicia', 'Gambia', 'Gaza Strip', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Cyprus', 'North Korea', 'North Macedonia', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'RÃ©union Island', 'Saba', 'Saint BarthÃ©lemy', 'Saint Helena', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint-Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'SÃ£o TomÃ© and PrÃ­ncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Eustatius', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'Somaliland', 'South Africa', 'South Georgia and the South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard and Jan Mayen Islands', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Togo', 'Tokelau', 'Tonga', 'Trinidad & Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'UAE', 'UK', 'USA', 'United States Virgin Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wallis and Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe'))


tld=countries[c_name]
tld=tld.replace(".","")
g_link='https://www.google.com/search?gl='+tld+'&q='



# In[75]:



@st.cache
def getStemmedReview(review):
    
    review = review.lower()
    review = review.replace("<br /><br />"," ")
   

    #Tokenize
    tokens = tokenizer.tokenize(review)
    new_tokens = [token for token in tokens if token not in en_stopwords]

    
    cleaned_review = ' '.join(new_tokens)
    
    
    return cleaned_review


@st.cache(suppress_st_warning=True)
def titles(resp):
    st.write("first")
   
    results = []
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                "title": title,
                "link": link }
                results.append(item)
    
    return results

@st.cache(suppress_st_warning=True)
def req(URL,headers):
    resp=requests.get(URL,headers=headers)
    return resp


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"



query = st.text_input("Enter Query")

query = query.replace(' ', '+')

URL =g_link+query
   
headers = {"user-agent": USER_AGENT}
resp = req(URL,headers)

results=titles(resp)

# In[111]:




@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def mt(results):
    Z=[]
    final_titles=[]
    meta_titles=[]
    domains={}
    for r in results:
        
        x=r["title"]
        linked=r['link']
        info = tldextract.extract(linked)
        name=info.domain
        url=info.registered_domain
        st.write("Scraping"+" : " +linked)
        
        if(name not in domains.keys()):
            domains[name]=1
        else:
            domains[name]+=1
        if(domains[name]>4):
            continue
        new=''
        try:
            new=requests.get(linked, headers=headers)
        except:
            continue
        soup1 = BeautifulSoup(new.content, "html.parser")
        t=''
        if(soup1.find('title')!=None):
            t=soup1.find('title').text
            item = {"title": t,"link": linked }
            Z.append(item)
            t=t.lower()
            t=t.replace(url," ")
            t=t.replace(name," ")
    
        if(t!=''):
            final_titles.append(t)
        st.write("Title"+" : " +t)
        st.write("Length : " + str(len(t)))
        title = soup1.find("meta",  property="og:description")
        if title:
            meta=title["content"]
            meta=meta.lower()
            st.write("Meta Description : " + meta )
            meta_titles.append(meta)
    return final_titles,meta_titles,Z

final_titles,meta_titles,Z=mt(results)    
# %%
i=0
for title in final_titles:
    z=getStemmedReview(title)
    res = ''.join([i for i in z if not i.isdigit()]) 
    final_titles[i]=res
    i+=1
i=0
for title in meta_titles:
    z=getStemmedReview(title)
    res = ''.join([i for i in z if not i.isdigit()]) 
    meta_titles[i]=res
    i+=1


bag1=[]
bag2=[]




st.write(Z)


# In[114]:


for title in final_titles:
    splitted=title.split(" ")
    for word in splitted:
        if(word is not ''):
            bag1.append(word)


# In[115]:


for title in meta_titles:
    splitted=title.split(" ")
    for word in splitted:
        if(word is not ''):
            bag2.append(word)


# In[116]:


word2count1 = {} 
for word in bag1: 
    if word not in word2count1.keys():
        word2count1[word]=1
    else:
        word2count1[word]+=1


# In[117]:


word2count2 = {} 
for word in bag2: 
    if word not in word2count2.keys():
        word2count2[word]=1
    else:
        word2count2[word]+=1


# In[118]:


a = sorted(word2count1.items(), key=lambda x: x[1],reverse=True)    
b = sorted(word2count2.items(), key=lambda x: x[1],reverse=True)    


# In[119]:


x=np.array(a)
y=np.array(b)



final1=pd.DataFrame(x, columns=['Word ','Frequency'])

final2=pd.DataFrame(y, columns=['Word ','Frequency'])


# In[124]:
st.title('Titles')
st.write(final1)


# In[ ]:


st.title('Meta Description')
st.write(final2)

st.text("--------------------------------------------")
st.text("--------------------------------------------")
st.text("Step 3: Analyze the Word Frequency Data Table. Select suitable words.")
st.text("Step 4: Input your selected words into interactive framework meta title builder")
st. text("Step 5: Tweak the Meta Title for any major grammatical error")
st. text("Step 6: Use the Meta Title for your important page. Repeat for new query.")
st.text("--------------------------------------------")
st.text ("Made by Saurabh Pandey. Get in touch with the makers at pandeysaurabh335@gmail.com or anubhav.limetray@gmail.com")



st.text("--------------------------------------------")
st.text("--------------------------------------------")
st.title("FRAMEWORK 1 INPUTS")
def get_output():
    d=[]
    name_dict = {"Format/Content Type (Ebook, Infographic, How-to.)":"", "Emotion (Hook The Visitor)":"","Promise (Something Valuable)":"","Topic (EAT)":""}
    j=0
    l=[]
    for k, v in name_dict.items():
        name_dict[k] = st.text_input(k," ",key=str(j))
        j+=1
        l.append(name_dict[k])
            
    final=' '.join(l)
    length=len(final)
    l.append(final)
    l.append(length-5)
    d.append(l)
    return d




def get_output2():
    d=[]
    st.text("--------------------------------------------")
    st.text("--------------------------------------------")
    st.title("FRAMEWORK 2 INPUTS")
    st.text("--------------------------------------------")
    name_dict = {"Focus Topic/Feature":"", "Benefit For Visitor":"","CTA (Learn / Know/ Get":""}
    j=100
    l=[]
    for k, v in name_dict.items():
        name_dict[k] = st.text_input(k," ",key=str(j))
        j+=1
        l.append(name_dict[k])
            
    final=' '.join(l)
    length=len(final)
    l.append(final)
    l.append(length-2)
    d.append(l)
    return d
    
st.text("--------------------------------------------")
st.text("--------------------------------------------")


d=get_output()

A=np.array(d)
T1=(A[0][:4])
T1=T1.reshape((1,4))


d2=get_output2()
A2=np.array(d2)
T2=(A2[0][:3])
T2=T2.reshape((1,3))


options = ("1", "2")

a = st.empty()
value = a.radio("Framework", options, 0,key="saurabh")

if value == '1':
    final3=pd.DataFrame(T1, columns=['Format/Content Type (Ebook, Infographic, How-to.)','Emotion (Hook The Visitor)','Promise (Something Valuable)','Topic (EAT)'])

    f=st.table(final3)
    final= A[0][4]
    length=int(A[0][5])-4
    item1 = {"Final": final,"Length":length }
    st.write(item1)
    st.text('Table')
    st.write(f)
elif value == '2':
    final4=pd.DataFrame(T2, columns=['Focus Topic/Feature ','Benefit For Visitor',' CTA'])
    f2=st.table(final4)
    final2=A2[0][3]
    length2=int(A2[0][4])-3
    item2 = {"Final": final2,"Length":length2 }
    st.write(item2)
    st.text('Table')

    st.write(f2)    


