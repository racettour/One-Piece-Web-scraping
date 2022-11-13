import requests as rq
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import tkinter as tk
import webbrowser

# variable loading
with open('listEp.pkl', 'rb') as file:
    # Call load method to deserialze
    last_listEp = pickle.load(file)


# To fake a web browser
navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'

# site url
url = "https://www.scan-vf.net/one_piece"

# scan website
html = rq.get(url, headers={'User-Agent': navigator})
soup = BeautifulSoup(html.text, 'html.parser')

# find all class named 'chapter-title-rtl'
encard = soup.find_all(class_='chapter-title-rtl')


# loop on boxes to create a dict with episode name and its hyperlink
list_episode = {}
for i_episode in encard:
    toto = i_episode.find('a', href=True).text
    tata = i_episode.find('a', href=True).attrs['href']
    list_episode[toto] = tata

# transform dict to dataframe
df_episode = pd.DataFrame(data=list_episode, index=['hyperlink'])
df_episode = df_episode.transpose()

# save df_episode
with open('listEp.pkl', 'wb') as file:
    # A new file will be created
    pickle.dump(df_episode, file)

# look for differences with the previous data
dif = df_episode.index.difference(last_listEp.index)


list_dif = dif.values
text = ''

for i_dif in list_dif:
    text += str(i_dif) + " : " + df_episode.loc[i_dif].values[0] + '\n'

print(text)


# graph part
root = tk.Tk()
root.title('unread episode')
root.geometry('400x300')
btn = []  # creates list to store the buttons ins

i = 0
for i_list_dif in list_dif:
    bts = tk.Button(root, text=i_list_dif,
                    command=lambda c=i_list_dif: webbrowser.open_new(df_episode.loc[c].values[0]))
    btn.append(bts)
    btn[i].pack()  # this packs the buttons
    i += 1

root.mainloop()

print('end')
