import requests
import tkinter as tk
import webbrowser
from dotenv import load_dotenv 
import os

#load environment variable
def configure():
    load_dotenv()


# global list to hold all fetched articles
articles = []
selected_category = "business"


def getNews():
    global articles
    api_key = os.getenv('api_key')
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={selected_category}&apiKey={(api_key)}"
    
    try:
        response = requests.get(url)
        news = response.json()

        if "articles" not in news:
            display_text("Failed to fetch news.")
            return

        articles = news["articles"]
        display_articles(articles)

    except Exception as e:
        display_text(f"Error: {str(e)}")

def display_articles(article_list):
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)

    for i, article in enumerate(article_list[:10]):
        title = article.get("title", "No Title")
        url = article.get("url", "")

        tag_name = f"link{i}"
        text_area.insert(tk.END, f"{i+1}. ", "bold")
        start = text_area.index(tk.END)
        text_area.insert(tk.END, title + "\n\n", tag_name)

        text_area.tag_config(tag_name, foreground="blue", underline=True)
        text_area.tag_bind(tag_name, "<Button-1>", lambda e, link=url: webbrowser.open(link))

    text_area.config(state=tk.DISABLED)

def display_text(content):
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)

def search_articles():
    search_term = search_entry.get().lower()
    filtered = [a for a in articles if search_term in a['title'].lower()]
    display_articles(filtered)

def on_category_change(*args):
    global selected_category
    selected_category = category_var.get().lower()
    getNews()

# --- GUI starts here ---
configure()

canvas = tk.Tk()
canvas.geometry("1400x800")
canvas.title("News app")

# --- Category Dropdown ---
category_frame = tk.Frame(canvas)
category_frame.pack(pady=10)

category_label = tk.Label(category_frame, text="Category:", font=("Helvetica", 16))
category_label.pack(side=tk.LEFT)

categories = ["Business", "Technology", "Health", "Science", "Sports", "Entertainment", "General"]
category_var = tk.StringVar()
category_var.set("Business")
category_menu = tk.OptionMenu(category_frame, category_var, *categories, command=on_category_change)
category_menu.config(font=("Helvetica", 14))
category_menu.pack(side=tk.LEFT, padx=10)

# --- Search bar ---
search_frame = tk.Frame(canvas)
search_frame.pack(pady=10)
search_label = tk.Label(search_frame, text="Search:", font=("Helvetica", 16))
search_label.pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, font=("Helvetica", 18), width=50)
search_entry.pack(side=tk.LEFT, padx=10)
search_button = tk.Button(search_frame, text="Search", command=search_articles)
search_button.pack(side=tk.LEFT)

# --- Refresh button ---
button = tk.Button(canvas, font=("Helvetica", 24), text="Refresh news", command=getNews)
button.pack(pady=20)

# --- Text display area with scrollbar ---
text_frame = tk.Frame(canvas)
text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(
    text_frame, font=("Helvetica", 16), wrap=tk.WORD,
    yscrollcommand=scrollbar.set, cursor="arrow"
)
text_area.pack(fill=tk.BOTH, expand=True)
text_area.tag_config("bold", font=("Helvetica", 16, "bold"))

scrollbar.config(command=text_area.yview)
text_area.config(state=tk.DISABLED)

# --- Initial fetch ---
getNews()

canvas.mainloop()
