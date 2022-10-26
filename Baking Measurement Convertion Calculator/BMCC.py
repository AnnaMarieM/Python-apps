import unicodedata
from fractions import Fraction

from recipe_scrapers import scrape_me

import tkinter as tk
import customtkinter
import re


def fraction_to_float(fraction):
    fraction = fraction.replace("⁄", "/")

    try:
        # amount je pouze unicode zlomek
        fraction_out = unicodedata.numeric(fraction)
    except:
        try:
            # amount je složený zlomek
            fraction_out = float(sum(Fraction(s) for s in fraction.split()))
        except:
            # amount je složený zlomek obsahující unicode znak
            fraction_split = fraction.split()
            fraction_out = float(fraction_split[0]) + unicodedata.numeric(fraction_split[1])
    return fraction_out


def string_to_float(string):
    try:
        window.output = float(string)
    except:
        window.output = None
    return window.output


def round_to_0_or_5(num):
    num = 5 * round(num/5)
    return num


def imperial_weight_to_metric(ingredients):
    for i in range(len(ingredients)):

        # unce na gramy
        if "ounce" in ingredients[i]:
            extract = (ingredients[i].split("ounce")[0])

            try:
                # převod str na float - složené číslo
                old_str = extract + "ounce"
                new_str = str(round_to_0_or_5(fraction_to_float(extract.strip()) * 28.3495231)) + " gram"
                ingredients[i] = ingredients[i].replace(old_str, new_str)
                #print(new_ingredinets)

            except:
                ingredients[i] = ingredients[i]

        # libry na gramy
        elif "pound" in ingredients[i]:
            extract = (ingredients[i].split("pound")[0])

            try:
                # převod str na float - složené číslo
                old_str = extract + "pound"
                new_str = str(round_to_0_or_5(fraction_to_float(extract.strip()) * 453.59237)) + " gram"
                ingredients[i] = ingredients[i].replace(old_str, new_str)
                #print(new_ingredinets)

            except:
                ingredients[i] = ingredients[i]
                
                
def imperial_volume_to_metric(ingredients):
    for i in range(len(ingredients)):
    
        # lžíce na mililitry
        if ("tablespoons" in ingredients[i]):
            extract = (ingredients[i].split("tablespoons")[0])

            try:
                # převod str na float - složené číslo      
                old_str = extract + "tablespoons"
                new_str = str(round_to_0_or_5(fraction_to_float(extract.strip()) * 14.7867648)) + " mililiters"
                ingredients[i] = ingredients[i].replace(old_str, new_str)
                #print(new_ingredinets)

            except:
                ingredients[i] = ingredients[i]


        # hrnky na mililitry
        elif "cup" in ingredients[i]:
            extract = (ingredients[i].split("cup")[0])

            try:
                # převod str na float - složené číslo
                old_str = extract + "cup"
                new_str = str(round_to_0_or_5(fraction_to_float(extract.strip()) * 236.588237)) + " mililiter"
                ingredients[i] = ingredients[i].replace(old_str, new_str)
                #print(new_ingredinets)

            except:
                ingredients[i] = ingredients[i]    
                
                
def volume_to_grams(ingredients):
    for i in range(len(ingredients)):
    
        if "mililiter" in ingredients[i]:
            if "oat" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.35)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]             
            
            elif "semolina" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.75)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]                  
            
            elif "flour" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.529)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
                    
            elif "sugar" in ingredients[i]:
                if ("confectioner's sugar" in ingredients[i]) or ("powdered sugar" in ingredients[i]) or ("icing sugar" in ingredients[i]):
                    extract = (ingredients[i].split("mililiter")[0])
                    try:
                        old_str = extract + "mililiter"
                        new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.49)) + " gram"
                        ingredients[i] = ingredients[i].replace(old_str, new_str)
                    except:
                        ingredients[i] = ingredients[i]    
                else:
                    extract = (ingredients[i].split("mililiter")[0])
                    try:
                        old_str = extract + "mililiter"
                        new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.88)) + " gram"
                        ingredients[i] = ingredients[i].replace(old_str, new_str)
                    except:
                        ingredients[i] = ingredients[i]
                        
            elif ("buttermilk" in ingredients[i]):
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()))) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
                    
            elif ("peanut butter" in ingredients[i]):
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 1.05)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
    

            elif ("butter" in ingredients[i]) or ("banana" in ingredients[i]) or ("oil" in ingredients[i]) or ("margarine" in ingredients[i]):
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.95)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
                    
            elif "shortening" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.83)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
                    
            elif "chocolate chips" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.72)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
        
                    
            elif "cocoa" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.507)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
 
            elif "cream" in ingredients[i]:
                if "whipping cream" in ingredients[i]:
                    extract = (ingredients[i].split("mililiter")[0])
                    try:
                        old_str = extract + "mililiter"
                        new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.97)) + " gram"
                        ingredients[i] = ingredients[i].replace(old_str, new_str)
                    except:
                        ingredients[i] = ingredients[i]    
                elif "sour cream" in ingredients[i]:
                    extract = (ingredients[i].split("mililiter")[0])
                    try:
                        old_str = extract + "mililiter"
                        new_str = str(round_to_0_or_5(string_to_float(extract.strip()))) + " gram"
                        ingredients[i] = ingredients[i].replace(old_str, new_str)
                    except:
                        ingredients[i] = ingredients[i]   
                elif "cream cheese" in ingredients[i]:
                    extract = (ingredients[i].split("mililiter")[0])
                    try:
                        old_str = extract + "mililiter"
                        new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.95)) + " gram"
                        ingredients[i] = ingredients[i].replace(old_str, new_str)
                    except:
                        ingredients[i] = ingredients[i]         
                else:
                    ingredients[i] = ingredients[i]
                          
            elif "cornstarch" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 0.55)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]       
                
            elif "honey" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()) * 1.435)) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]
               
            elif "yoghurt" in ingredients[i]:
                extract = (ingredients[i].split("mililiter")[0])
                try:
                    old_str = extract + "mililiter"
                    new_str = str(round_to_0_or_5(string_to_float(extract.strip()))) + " gram"
                    ingredients[i] = ingredients[i].replace(old_str, new_str)
                except:
                    ingredients[i] = ingredients[i]     
                    
                    
def parentheses_in_the_recipe_imperial_to_metric(ingredients):
    for i in range(len(ingredients)):
        if "(" in ingredients[i]:
            str_ing = str(ingredients[i])
            extract = (str_ing.split("(")[1])
            list_ex = list(extract.split(")"))

            try:
                imperial_volume_to_metric(list_ex)
                imperial_weight_to_metric(list_ex)
                new_str = list_ex[0] + ")" + list_ex[1]
                ingredients[i] = ingredients[i].replace(extract, new_str)

            except:
                ingredients[i] = ingredients[i] 
                
                
def parentheses_in_the_recipe_volume_to_grams(ingredients):
    for i in range(len(ingredients)):
        if "(" in ingredients[i]:
            str_ing = str(ingredients[i])
            extract = (str_ing.split("(")[1])
            list_ex = list(extract.split("      "))

            try:
                volume_to_grams(list_ex)
                new_str = list_ex[0]
                ingredients[i] = ingredients[i].replace(extract, new_str)

            except:
                ingredients[i] = ingredients[i]         
                
                
def gram_grams_to_g(ingredients):
    for i in range(len(ingredients)):
    
        if "grams" in ingredients[i]:
            ingredients[i] = ingredients[i].replace("grams", "g")
        elif "gram" in ingredients[i]:
            ingredients[i] = ingredients[i].replace("gram", "g")      
            
def mililiter_mililiters_to_g(ingredients):
    for i in range(len(ingredients)):
    
        if "mililiters" in ingredients[i]:
            ingredients[i] = ingredients[i].replace("mililiters", "ml")
        elif "mililiter" in ingredients[i]:
            ingredients[i] = ingredients[i].replace("mililiter", "ml")   
            
            
def convertion(ingredients): 
    imperial_weight_to_metric(ingredients)
    imperial_volume_to_metric(ingredients)
    volume_to_grams(ingredients)
    parentheses_in_the_recipe_imperial_to_metric(ingredients)
    parentheses_in_the_recipe_volume_to_grams(ingredients)
    gram_grams_to_g(ingredients)
    mililiter_mililiters_to_g(ingredients)
    


# In[30]:


def widget_output():
    ent = url.get()
    if (ent == "Site is not supported. Input recipe ingredients manually.") or (ent == "") or (ent == " ") or (ent == "\n") or (ent == "Please enter url"):
        i = entry.get(1.0, tk.END + "-1c")
        ingredients = i.split("\n") 
        output.delete(0.0,tk.END)
        convertion(ingredients)
        for i in range(len(ingredients)):
            output.insert(tk.END,ingredients[i] + "\n")
        
    else:    
        try:
            entry.delete(0.0,tk.END)
            output.delete(0.0,tk.END)
            scraper = scrape_me(ent.strip() , wild_mode = True)
            title = scraper.title()
            ingredients = scraper.ingredients()
            entry.insert(tk.END, title + " - original" + "\n")
            for i in range(len(ingredients)):
                entry.insert(tk.END, "\n" + ingredients[i])  
            convertion(ingredients)
            output.insert(tk.END, title + " - converted" + "\n")    
            for i in range(len(ingredients)):
                output.insert(tk.END,"\n" + ingredients[i])
            return ingredients

        except:
            url.delete(0, tk.END)
            url.insert(0, "")
            url.insert(tk.END, "Site is not supported. Input recipe ingredients manually.")
            
def save_output():
    name = output.get(1.0, tk.END)
    
    
    if "- converted" in name:
        dany_nazev = name.split("- converted")[0]
        name = new_window_11(dany_nazev).strip()
        file = open(name + ".txt", "w", encoding="utf-8") 
        recipe = output.get(1.0, tk.END)
        file.write(recipe) 
        file.close()
        
    else:
        if not name.strip():
            url.delete(0, tk.END)
            url.insert(0, "")
            url.insert(tk.END, "Nothing to be saved.")

        else:
            name = new_window_12().strip()
            file = open(name + ".txt", "w", encoding="utf-8") 
            recipe = output.get(1.0, tk.END)
            file.write(recipe) 
            file.close() 


def new_window_11(dany_nazev):
    root = customtkinter.CTk()
    root.geometry("350x190")
    name = tk.StringVar()

    def submit():
        name.set(entry.get())

    label = customtkinter.CTkLabel(root, text= "Save as:", text_font = ("Roboto", -19))
    label.grid(row = 1, column=1, pady=20, padx=30, sticky = "we")

    entry = customtkinter.CTkEntry(root, width =70, placeholder_text = " ", text_font = ("Roboto", -20),)
    entry.grid(row = 2, column=1, pady=0, padx=30, sticky = "we")
    entry.insert(tk.END, dany_nazev)
    entry.focus()


    sub =  customtkinter.CTkButton(root, text = "Submit", command = lambda: [submit(), root.quit(), root.destroy()], border_width = 1, fg_color = None, text_font = ("Roboto", -19))
    sub.grid(row = 3, column=1, pady=25, padx=100, sticky = "we")

    root.resizable(False,False)  
    root.mainloop()    

    return name.get()


def new_window_12():
    root = customtkinter.CTk()
    root.geometry("350x190")
    name = tk.StringVar()

    def submit():
        name.set(entry.get())

    label = customtkinter.CTkLabel(root, text= "Save as:", text_font = ("Roboto", -19))
    label.grid(row = 1, column=1, pady=20, padx=30, sticky = "we")

    entry = customtkinter.CTkEntry(root, width =70, placeholder_text = " ", text_font = ("Roboto", -20),)
    entry.grid(row = 2, column=1, pady=0, padx=30, sticky = "we")
    entry.focus()


    sub =  customtkinter.CTkButton(root, text = "Submit", command = lambda: [submit(), root.quit(), root.destroy()], border_width = 1, fg_color = None, text_font = ("Roboto", -19))
    sub.grid(row = 3, column=1, pady=25, padx=100, sticky = "we")

    root.resizable(False,False)  
    root.mainloop()    

    return name.get()


            
def resize_recipe():
    scale = fraction_to_float(new_window_2().strip())
    
    i = entry.get(1.0, tk.END + "-1c")
    ingredients = i.split("\n") 
    convertion(ingredients)
    
    resize(ingredients, scale)  
    
    round_for_resize(ingredients)
    
    output.delete(0.0,tk.END)
    
    for i in range(len(ingredients)):
        output.insert(tk.END,ingredients[i] + "\n")
        
    if scale > 1:
        output.insert(tk.END, "\n" + "larger batch recipe")
        
    if scale < 1:
        output.insert(tk.END, "\n" + "smaller batch recipe")
        
    

import re
def multiply(num, scale):
    def sub(i):
        return str(int(i.group(0))*scale)
    return re.sub('[0-9]+', sub, num)


def resize(ingredients, scale):
    s = [" ml ", " g ", " tbsp ", " Tbsp ", " Tb ", " tsp ", " tablespoon ", " teaspoon ", " teaspoons "]
    for i in range(len(ingredients)):
        if any(j in ingredients[i] for j in s):
            for k in range(len(s)):
                if s[k] in ingredients[i]:
                
                    old_str = (ingredients[i].split(s[k])[0])

                    new = fraction_to_float(old_str.strip()) * scale
                    if new < 1:
                        new_str = str(new) 
                    else:
                        new_str = str(int(new)) 
                    ingredients[i] = ingredients[i].replace(old_str, new_str)

        else:   
            ingredients[i] = multiply(ingredients[i], scale)
            
        if "original" in ingredients[i]:
            ingredients[i] = ingredients[i].replace("original", "converted")
            
            

def round_for_resize(ingredients):
    for i in range(len(ingredients)):
        cislo = re.findall("\d+\.\d+", ingredients[i])
        if len(cislo) == 1:
            round_num = str(round(float(cislo[0]), 2))
            
            ingredients[i] = ingredients[i].replace(str(cislo[0]), round_num)


def new_window_2():
    root = customtkinter.CTk()
    root.geometry("455x200")
    scale = tk.StringVar()
    scale.set("1")

    def submit():
        scale.set(entry.get())

    label = customtkinter.CTkLabel(root, text= "Scale (for larger batch enter for example 2.0 or \nfor smaller batch enter for example 0.5 or 1/2):", text_font = ("Roboto", -19))
    label.grid(row = 1, column=1, pady=20, padx=30, sticky = "we")

    entry = customtkinter.CTkEntry(root, width =70, placeholder_text = " ", text_font = ("Roboto", -20),)
    entry.grid(row = 2, column=1, pady=0, padx=30, sticky = "we")
    entry.focus()

    sub =  customtkinter.CTkButton(root, text = "Submit", command = lambda: [submit(), root.quit(), root.destroy()], border_width = 1, fg_color = None, text_font = ("Roboto", -19))
    sub.grid(row = 3, column=1, pady=25, padx=100, sticky = "we")

    root.resizable(False,False)  
    root.mainloop()    

    return scale.get()


def clean():
    url.delete(0,tk.END)
    entry.delete(1.0,tk.END)
    #output.config(state = "normal")
    output.delete(1.0,tk.END)


# In[31]:


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


window = customtkinter.CTk()
width  = 640
height = 650
window.geometry(f'{width}x{height}')
window.title("Recipe converter")
    
# vstup
    

url = customtkinter.CTkEntry(master = window, width = 580, placeholder_text = "", text_font = ("Roboto", -20))#, textvar = textin)
url.grid(row = 8, column = 0, columnspan = 6, pady = 30, padx = (30,0), sticky = "we")
url.focus()
url.insert(0, "Please enter url")

# tlačítka

# 1
button =  customtkinter.CTkButton(master = window, text = "Convert", border_width = 1, fg_color = None, 
                                    command = widget_output, text_font = ("Roboto", -19))
button.grid(row = 9, column=1, pady=0, padx=(30,0), sticky = "we")

#2
button = customtkinter.CTkButton(master = window, text = "Save recipe", border_width = 1, fg_color = None, 
                                        command = save_output, text_font = ("Roboto", -19))
button.grid(row = 9, column=2, pady=0, padx=0, sticky = "we")

# 3
button = customtkinter.CTkButton(master = window, text = "Resize recipe", border_width = 1, fg_color = None, 
                                    command = resize_recipe, text_font = ("Roboto", -19))
button.grid(row = 9, column=3, pady=0, padx=0, sticky = "we")

#4
button = customtkinter.CTkButton(master = window, text = "Clean", border_width = 1, fg_color = None, 
                                        command = clean, text_font = ("Roboto", -19))
button.grid(row = 9, column=4, pady=0, padx=0, sticky = "we")




# vstupní pole
entry = customtkinter.CTkTextbox(master = window, height = 470, width = 289, corner_radius=6, bd = 0, border_color = "black", text_font = ("Roboto", -20), 
                                      wrap = tk.WORD)
entry.grid(row = 10, column=1, columnspan = 2, pady=30, padx=(30,0), sticky = "we")

# výstupní pole
output = customtkinter.CTkTextbox(master = window, height = 470, width = 289, corner_radius=6, bd = 0, border_color = "black", text_font = ("Roboto", -20), 
                                      wrap = tk.WORD)
output.grid(row = 10, column=3, columnspan = 2, pady=30, padx=0, sticky = "we")


window.resizable(False,False) 
window.mainloop()


