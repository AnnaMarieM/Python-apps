from bs4 import BeautifulSoup
import requests
import html5lib

import re

import pandas as pd
import math

import tkinter as tk
import customtkinter
from tkinter import filedialog, messagebox, ttk



# vyhledání zadaného stringu na MusicBrainz, url odkaz na první výsledek vyhledávání

def get_url_to_MusicBrainz_from_string_first_link(string):
    url1 = "https://musicbrainz.org/search?query=" + string.replace(" ", "+") + "&type=artist&method=indexed"
    
    soup = BeautifulSoup(requests.get(url1, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').select("table tr a")[0]
    artist = soup.text
    url = "https://musicbrainz.org" + soup.get("href")
    
    return artist, url




# vyhledání zadaného stringu, pokud na první pozici není požadovaný umělec, jsou vypsáni vyhledaní umělci a uživatelem je vybrán správný výsledek

def get_url_to_MusicBrainz_from_string_chosen_link(string):
    url1 = "https://musicbrainz.org/search?query=" + string.replace(" ", "+") + "&type=artist&method=indexed"
    
    soup = BeautifulSoup(requests.get(url1, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').select("table tr a")
    
    new_soup = []
    names = []
    
    for i in range(len(soup)):
        if soup[i].get("title") is not None:
            new_soup.append(soup[i])
            names.append(soup[i].get("title"))
    
    for (i, item) in enumerate(names, start = 1):
        print(i, item)
        
    i = int(input()) - 1
    soup = new_soup[i]
    
    artist = soup.text
    url = "https://musicbrainz.org" + soup.get("href")
    
    return artist, url




# pomocí url na stránku umělce, tam získání informací o všech albech (název, rok, hodnocení) a vytvoření dataframu s těmito informacemi

def list_of_albums_get_from_MusicBrainz(url):
    
    # načtení stránky podle url, najití první tabulky (alba)
    tab = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').find("table") 
    
    df = pd.DataFrame(pd.read_html(str(tab))[0])[["Title", "Year", "Releases", "Rating"]]
    
    # přidání odkazů na jednotlivá alba na MusicBrainz
    soups = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').find("table", {"class":"tbl release-group-list"}).find_all("a")
    soup = []
    for i in range(len(soups)):
        if "release-group" in soups[i].get("href"):
            soup.append("https://musicbrainz.org" + soups[i].get("href"))
     
    df = df.assign(MusicBrainz_url = soup).rename(columns = {"MusicBrainz_url": "url MusicBrainz"})
    # odstranění "nevydaných" (Releases = 0), přejmenování MusicBrainz hodnocení, NaN za 0.0
    df = df[df["Releases"] != 0.0].rename(columns = {"Rating": "Rating MusicBrainz"}).replace(math.nan, 0)
    return df




# url AllMusic

def get_reviews_from_AllMusic_using_url(url):
    soup = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').find("ul",{"class":"ratings"})
    try:
        AllMusicRating = int(soup.find("li",{"id":"microdata-rating"}).find("div").text.strip()) / 2
    except:
        AllMusicRating = "-"
    
    return AllMusicRating




# vyhledání alba na AllMusic, nalezení správného alba pomocí srovnání s interpretem

def search_for_url_AllMusic(album, artist):
    url = "https://www.allmusic.com/search/albums/" + album.replace(" ", "%20").replace("/", "__")
    soup = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).content, "html.parser").find_all("li",{"class":"album"})

    for i in range(len(soup)):
        a = soup[i].find("div",{"class":"artist"}).text.strip()

        if a == artist: 
            url = soup[i].find("div", {"class":"title"}).find("a").get("href")
            break
            
    return url




def get_reviews_from_other_pages_Allmusic(df, artist):
    urls = list(df["url MusicBrainz"])
    
    
    url_AllMusic = []
    hodnoceni_AllMusic = []

    for i in range(len(urls)):
        soup = BeautifulSoup(requests.get(urls[i], headers = {'User-agent': 'your bot 0.1'}).content, "html.parser").find("div",{"id":"sidebar"}).find_all("ul", {"class":"external_links"})
       
        if len(soup) != 0:
            u_A = soup[0].find("li",{"class":"allmusic-favicon"})

            if not u_A:
                    album = df["Title"][i]
                    u_A = search_for_url_AllMusic(album, artist)
                    url_AllMusic.append(u_A)
                    hodnoceni_AllMusic.append(get_reviews_from_AllMusic_using_url(u_A))
                    
            else:
                u_A = u_A.find("a").get("href")
                url_AllMusic.append(u_A)
                hodnoceni_AllMusic.append(get_reviews_from_AllMusic_using_url(u_A))
                
        else:
            album = df["Title"][i]
            u_A = search_for_url_AllMusic(album, artist)
            url_AllMusic.append(u_A)
            hodnoceni_AllMusic.append(get_reviews_from_AllMusic_using_url(u_A))
                    


    df = df.assign(hodnoceni_AllMusic = hodnoceni_AllMusic).rename(columns = {"hodnoceni_AllMusic": "Rating AllMusic"})  
    df = df.assign(url_AllMusic = url_AllMusic).rename(columns = {"url_AllMusic": "url AllMusic"})  
        
    return df




# url Discogs

def get_reviews_from_Discogs_using_url(url):
    try:
        soup = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').find_all("div",{"class":"items_Y-X8L"})[1].text
        number_of_reviewers = soup.split(":")[2]
    
        rating = float(soup.split(":")[1].split("/")[0].strip())
        
    except:
        try:
            soup = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').find_all("div",{"class":"items_3gMeU"})[0].text            
            number_of_reviewers = soup.split("Ratings:")[1].split("Last")[0].strip()

            rating = float(soup.split("Rating:")[1].split("/")[0].strip())
        
        except:
            rating = 0.0
            number_of_reviewers = "-"
    
    return rating, number_of_reviewers




# vyhledání alba na Discogs, nalezení správného alba pomocí srovnání s interpretem

def search_for_url_Discogs(album, artist):
    url = "https://www.discogs.com/search/?q=" + album.replace(" ", "+").replace("/", "%2F") + "&type=all&format_exact=Album"
    soup = BeautifulSoup(requests.get(url, headers = {'User-agent': 'your bot 0.1'}).content, "html.parser").find_all("li",{"role":"listitem"})

    for i in range(len(soup)):
        a = soup[i].find("div",{"class":"card-artist-name"}).text.strip()
        if a == artist: 

            url = "https://www.discogs.com" + soup[i].find("div", {"class":"card-release-title"}).find("a").get("href")
            break
            
    return url




def get_reviews_from_other_pages_Discogs(df, artist):
    urls = list(df["url MusicBrainz"])
    
    url_discogs = []
    hodnoceni_discogs = []
    pocet_hodnotitelu_discogs = []

    for i in range(len(urls)):
        soup = BeautifulSoup(requests.get(urls[i], headers = {'User-agent': 'your bot 0.1'}).content, "html.parser").find("div",{"id":"sidebar"}).find_all("ul", {"class":"external_links"})
        
        if len(soup) != 0:
            u_D = soup[0].find("li",{"class":"discogs-favicon"})
            
            if not u_D:
                album = df["Title"][i]
                u_D = search_for_url_Discogs(album, artist)
                url_discogs.append(u_D)
                r, n = get_reviews_from_Discogs_using_url(u_D)
                hodnoceni_discogs.append(r)
                pocet_hodnotitelu_discogs.append(n)

                
            else:    
                u_D = u_D.find("a").get("href")

                url_discogs.append(u_D)
                r, n = get_reviews_from_Discogs_using_url(u_D)
                hodnoceni_discogs.append(r)
                pocet_hodnotitelu_discogs.append(n)


        else:
            album = df["Title"][i]
            u_D = search_for_url_Discogs(album, artist)
            url_discogs.append(u_D)
            r, n = get_reviews_from_Discogs_using_url(u_D)
            hodnoceni_discogs.append(r)
            pocet_hodnotitelu_discogs.append(n)
            
            
    df = df.assign(hodnoceni_discogs = hodnoceni_discogs).rename(columns = {"hodnoceni_discogs": "Rating Discogs"}) 
    df = df.assign(pocet_hodnotitelu_discogs = pocet_hodnotitelu_discogs).rename(columns = {"pocet_hodnotitelu_discogs": "Počet hodnocení Discogs"})   
    df = df.assign(url_discogs = url_discogs).rename(columns = {"url_discogs": "url Discogs"}) 
        
    return df




def reorganise_dataframe(df):
    try:
        df = df[["Title", "Year", "Releases", "Rating MusicBrainz", "Rating AllMusic", "Rating Discogs", "Počet hodnocení Discogs", "url MusicBrainz", "url AllMusic", "url Discogs"]]
    except:
        df = df
                                
    return df





customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


root = customtkinter.CTk()
root.state("zoomed")
root.title("AMMD")


# rozdělení na dvě části

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

root.frame_left = customtkinter.CTkFrame(master = root, width=180, corner_radius=0)
root.frame_left.grid(row = 0, column = 0, sticky = "nswe")

root.frame_right = customtkinter.CTkFrame(master = root)
root.frame_right.grid(row = 0, column = 1, sticky = "nswe", padx=20, pady=20)


# funkce

#search vázaný na enter

def search_1(e):
    string = root.entry.get()
    posledni = root.text.get("end-2c linestart","end").strip()
        
    try:
        artist, url = get_url_to_MusicBrainz_from_string_first_link(string)
        
    except:
        string = None
    
    if string == None:
        pass
    
    elif posledni.isnumeric():
        soup = n_soup[int(posledni) - 1]
    
        artist = soup.text
        url = "https://musicbrainz.org" + soup.get("href")
        
        df = list_of_albums_get_from_MusicBrainz(url)

        df = get_reviews_from_other_pages_Allmusic(df, artist)
        df = get_reviews_from_other_pages_Discogs(df, artist)
        #df = get_reviews_from_other_pages_RateYourMusic(df, artist)
        df = reorganise_dataframe(df)

        for i in tv.get_children():
            tv.delete(i)
        root.update()    
        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv.insert("", "end", values=row)     
            
        root.text.delete(1.0,tk.END)
        root.entry.delete(0,tk.END)
        root.entry.insert(0, artist)
        root.entry.focus()

        
    elif posledni != "y" and posledni != "n":
                
        root.text.insert(tk.END, artist + "\n" + "\n")
        root.text.insert(tk.END, "Is this your desired result? (y/n)" + "\n" + "\n")
        root.text.focus()
        
    elif posledni == "y":
        
        df = list_of_albums_get_from_MusicBrainz(url)
        
        df = get_reviews_from_other_pages_Allmusic(df, artist)
        df = get_reviews_from_other_pages_Discogs(df, artist)
        #df = get_reviews_from_other_pages_RateYourMusic(df, artist)
        df = reorganise_dataframe(df)

        for i in tv.get_children():
            tv.delete(i)
        root.update()    
        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv.insert("", "end", values=row)     
            
        root.text.delete(1.0,tk.END)
        root.entry.delete(0,tk.END)
        root.entry.insert(0, artist)
        root.entry.focus()
            
    else:
        new_soup = list_of_artists(string)
        root.text.focus()
        
root.bind('<Return>', search_1)

# search vázaný na tlačítko search

def search():
    string = root.entry.get()
    posledni = root.text.get("end-1c linestart","end").strip()
    
    try:
        artist, url = get_url_to_MusicBrainz_from_string_first_link(string)
        
    except:
        string = None
    
    if string == None:
        pass
    
    elif posledni.isnumeric():
        soup = n_soup[int(posledni) - 1]
    
        artist = soup.text
        url = "https://musicbrainz.org" + soup.get("href")
        
        df = list_of_albums_get_from_MusicBrainz(url)

        df = get_reviews_from_other_pages_Allmusic(df, artist)
        df = get_reviews_from_other_pages_Discogs(df, artist)
        #df = get_reviews_from_other_pages_RateYourMusic(df, artist)
        df = reorganise_dataframe(df)

        for i in tv.get_children():
            tv.delete(i)
        root.update()    
        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv.insert("", "end", values=row)     
            
        root.text.delete(1.0,tk.END)
        root.entry.delete(0,tk.END)
        root.entry.insert(0, artist)
        root.entry.focus()

        
    elif posledni != "y" and posledni != "n":
                
        root.text.insert(tk.END, artist + "\n" + "\n")
        root.text.insert(tk.END, "Is this your desired result? (y/n)" + "\n" + "\n")
        root.text.focus()
        
    elif posledni == "y":
        
        df = list_of_albums_get_from_MusicBrainz(url)

        df = get_reviews_from_other_pages_Allmusic(df, artist)
        df = get_reviews_from_other_pages_Discogs(df, artist)
        #df = get_reviews_from_other_pages_RateYourMusic(df, artist)
        df = reorganise_dataframe(df)

        for i in tv.get_children():
            tv.delete(i)
        root.update()    
        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv.insert("", "end", values=row)     
            
        root.text.delete(1.0,tk.END)
        root.entry.delete(0,tk.END)
        root.entry.insert(0, artist)
        root.entry.focus()
            
    else:
        new_soup = list_of_artists(string)
        root.text.focus()
        
        
# ukládání soup (na MusicBrainz, když uživatel nesouhlasí s prvním výsledkem) do globální proměnné
        
def myfunc(seznam):
    global n_soup
    n_soup = seznam
        

def list_of_artists(string):
    url1 = "https://musicbrainz.org/search?query=" + string.replace(" ", "+") + "&type=artist&method=indexed"
    
    soup = BeautifulSoup(requests.get(url1, headers = {'User-agent': 'your bot 0.1'}).text, 'html.parser').select("table tr a")
    
    new_soup = []
    names = []
    
    for i in range(len(soup)):
        if soup[i].get("title") is not None:
            new_soup.append(soup[i])
            names.append(soup[i].get("title"))
    
    root.text.insert(tk.END, "\n")
    for (i, item) in enumerate(names, start = 1):
        root.text.insert(tk.END, "\n" + str(i) + "   " + item)
    root.text.insert(tk.END, "\n \n")
    
    myfunc(new_soup)
    

# sortování podle všeho možného

# sort by name

index_title = 0
def alternate_for_title(n):
    global index_title
    index_title += 1 
    return index_title


def sort_title(): 
    num = alternate_for_title(index_title)
    
    if (num % 2) == 0:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Title")

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv.insert("", "end", values=row)  
            
    else:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Title")[::-1]

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows:
            tv.insert("", "end", values=row)  

# sorting by year
        
index_year = 0
def alternate_for_years(n):
    global index_year
    index_year += 1 
    return index_year
        
      
def sort_year():
    num = alternate_for_years(index_year)
    
    if (num % 2) == 0:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Year")

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist() 
        for row in df_rows:
            tv.insert("", "end", values=row)  
            
    else:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Year")[::-1]

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist() 
        for row in df_rows:
            tv.insert("", "end", values=row)  


# sorting by MusicBrainz rating

index_MB = 0
def alternate_for_MB(n):
    global index_MB
    index_MB += 1 
    return index_MB

def sort_MusicBrainz():
    num = alternate_for_MB(index_MB)
    
    if (num % 2) == 0:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Rating MusicBrainz")[::-1]

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist() 
        for row in df_rows:
            tv.insert("", "end", values=row)  
            
    else:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Rating MusicBrainz")

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist() 
        for row in df_rows:
            tv.insert("", "end", values=row)  
    
    
# sorting by AllMusic rating

index_AM = 0
def alternate_for_AM(n):
    global index_AM
    index_AM += 1 
    return index_AM


def sort_AllMusic():
    num = alternate_for_AM(index_AM)
    
    if (num % 2) == 0:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Rating AllMusic")[::-1]

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist()
        for row in df_rows:
            tv.insert("", "end", values=row)  
            
    else:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Rating AllMusic")

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist()
        for row in df_rows:
            tv.insert("", "end", values=row)  


# sorting by discogs

index_discogs = 0
def alternate_for_discogs(n):
    global index_discogs
    index_discogs += 1 
    return index_discogs


def sort_Discogs():
    num = alternate_for_discogs(index_discogs)
    
    if (num % 2) == 0:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Rating Discogs")[::-1]

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist()
        for row in df_rows:
            tv.insert("", "end", values=row)
            
    else:
        row_list = []
        columns = tv["columns"]
        for row in tv.get_children():
            row_list.append(tv.item(row)["values"])

        treeview_df = pd.DataFrame(row_list, columns = columns)
        treeview_df = treeview_df.sort_values("Rating Discogs")

        for i in tv.get_children():
            tv.delete(i)
        root.update()  
        df_rows = treeview_df.to_numpy().tolist()
        for row in df_rows:
            tv.insert("", "end", values=row)


# levá část

root.label_mode = customtkinter.CTkLabel(master = root.frame_left, text=" AMMD ", height = 60, corner_radius=6, 
                                         fg_color=("white", "#7393B3"), text_font = ("Roboto Medium", -30))
root.label_mode.grid(row = 1, column = 0, pady = 20, padx=10)



# pravá část
    
# vstup

root.entry = customtkinter.CTkEntry(master=root.frame_right, width= 350, placeholder_text = " Artist", text_font = ("Roboto", -20))
root.entry.grid(row=8, column=0, pady=20, padx=20, sticky="we")
root.entry.focus()


# tlačítka

root.button_1 = customtkinter.CTkButton(master = root.frame_right, text = " Search ", border_width = 1, fg_color = None, 
                                        command = search, text_font = ("Roboto", -19))
root.button_1.grid(row = 8, column=2, columnspan = 2, pady=20, padx=0, sticky = "we")


# podklad tabulky

root.label_mode_1 = customtkinter.CTkLabel(master = root.frame_right, text=" ", corner_radius=6, 
                                         fg_color=("white", "#7393B3"), heigh = 43, text_font = ("Roboto Medium", -10))
root.label_mode_1.grid(row=9, rowspan=3, column=0, sticky="nwe", padx=20, pady=0)


# tabulka

container_tree = tk.Frame(root.frame_right, width=1205, height=735)
container_tree.propagate(False)
container_tree.grid(row=9, column=0, sticky="nwe", padx=50, pady=(20,0))

tv = ttk.Treeview(container_tree, show='headings', height = 23, selectmode ='browse')
fr_y = tk.Frame(container_tree)
fr_y.pack(side='right', fill='y')
tk.Label(fr_y, borderwidth=1, relief='raised', font="Arial 8").pack(side='bottom', fill='x')

sb_y = tk.Scrollbar(fr_y, orient="vertical", command = tv.yview, width = 12)

sb_y.pack(expand = 'yes', fill='y')
fr_x = tk.Frame(container_tree)
fr_x.pack(side = 'bottom', fill='x')

sb_x = tk.Scrollbar(fr_x, orient="horizontal", command = tv.xview, width = 13)

sb_x.pack(expand='yes', fill='x')
tv.configure(yscrollcommand=sb_y.set, xscrollcommand = sb_x.set)
tv.pack(fill='both', expand='yes')


tv["columns"]=("Title", "Year", "Releases", "Rating MusicBrainz", "Rating AllMusic", "Rating Discogs", "Počet hodnocení Discogs")


tv.column('#0', width=5, stretch= tk.NO)
tv.column('Title', anchor= tk.CENTER, width=380)
tv.column('Year', anchor= tk.CENTER, width=70)
tv.column('Releases', anchor= tk.CENTER, width=100)
tv.column('Rating MusicBrainz', anchor= tk.CENTER, width=125)
tv.column('Rating AllMusic', anchor= tk.CENTER, width=100)
tv.column('Rating Discogs', anchor= tk.CENTER, width=100)
tv.column('Počet hodnocení Discogs', anchor= tk.CENTER, width=100)


style = ttk.Style()
style.configure("Treeview.Heading", font=("Roboto Medium", -20))
style.configure("Treeview", rowheight = 40)


tv.heading('#0', text='')
tv.heading('Title', anchor= tk.CENTER, text='Title', command = sort_title)
tv.heading('Year', anchor= tk.CENTER,text='Year', command = sort_year)
tv.heading('Releases', anchor= tk.CENTER, text='Releases', command = sort_year)
tv.heading('Rating MusicBrainz', anchor= tk.CENTER, text='MusicBrainz', command = sort_MusicBrainz)
tv.heading('Rating AllMusic', anchor= tk.CENTER, text='AllMusic', command = sort_AllMusic)
tv.heading('Rating Discogs', anchor= tk.CENTER, text='Discogs', command = sort_Discogs)
tv.heading('Počet hodnocení Discogs', anchor= tk.CENTER, text='# Discogs', command = sort_year)


tv.insert(parent='', index=0, iid=0, text='', values=('-','-','-','-','-','-','-','-','-','-','-','-','-','-'))

  


# opend url when double clicked

def link_tree(event):
    input_id = tv.selection()
    input_item = tv.item(input_id)["values"]
    url1 = input_item[len(input_item) - 3]
    url2 = input_item[len(input_item) - 2]
    url3 = input_item[len(input_item) - 1]

    import webbrowser
    webbrowser.open('{}'.format(url1))
    webbrowser.open('{}'.format(url2))
    webbrowser.open('{}'.format(url3))

    
tv.bind("<Double-1>", link_tree)



# text field far right
root.text = customtkinter.CTkTextbox(master = root.frame_right, height = 520, width = 190, corner_radius=6, bd = 0, border_color = "black", text_font = ("Roboto", -20), wrap = tk.WORD)

root.text.grid(row = 9, column=2, rowspan = 3, columnspan = 2, pady=0, padx=0, sticky = "we")



root.mainloop()