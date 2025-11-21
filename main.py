import os
import urllib.parse
import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
from pathlib import Path
import unicodedata
import json

API_KEY = os.environ.get("OMDB_API_KEY", "473ea196")
HISTORY_FILE = Path(__file__).resolve().parent / "search_history.json"

dark_mode = True
search_history = []
comparison_movies = []
current_movie_data = {}

def normalize_text(text):
    nfd_form = unicodedata.normalize('NFD', text)
    return ''.join(char for char in nfd_form if unicodedata.category(char) != 'Mn')

def create_rounded_button(parent, **kwargs):
    """Vytvoří zaoblené tlačítko s shadow efektem"""
    # Shadow frame
    shadow_frame = tk.Frame(parent, bg="#00000020", relief="flat", bd=0)
    
    # Actual button
    btn = tk.Button(
        shadow_frame,
        highlightthickness=0,
        bd=0,
        relief="flat",
        **kwargs
    )
    btn.pack(padx=2, pady=2)
    return shadow_frame, btn

def load_search_history():
    global search_history
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                search_history = json.load(f)[:10]
    except:
        search_history = []

def save_search_history(title):
    global search_history
    if title not in search_history:
        search_history.insert(0, title)
        search_history = search_history[:10]
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(search_history, f, ensure_ascii=False, indent=2)
        except:
            pass

def toggle_dark_mode():
    global dark_mode, BG_PRIMARY, BG_SECONDARY, BG_TERTIARY, TEXT_PRIMARY, TEXT_SECONDARY, ACCENT_BLUE, ACCENT_PURPLE, ACCENT_PINK, ACCENT_GREEN
    
    dark_mode = not dark_mode
    
    if dark_mode:
        # Dark mode
        BG_PRIMARY = "#0a0e27"
        BG_SECONDARY = "#161b35"
        BG_TERTIARY = "#1f2847"
        TEXT_PRIMARY = "#e8f0ff"
        TEXT_SECONDARY = "#a0b9d8"
        ACCENT_BLUE = "#00d4ff"
        ACCENT_PURPLE = "#bb86fc"
        ACCENT_PINK = "#ff4081"
        ACCENT_GREEN = "#00e676"
        theme_btn.config(text="🌙 Dark")
    else:
        # Light mode
        BG_PRIMARY = "#f8f9fc"
        BG_SECONDARY = "#eff2f8"
        BG_TERTIARY = "#ffffff"
        TEXT_PRIMARY = "#0f1419"
        TEXT_SECONDARY = "#3a4a6a"
        ACCENT_BLUE = "#0066dd"
        ACCENT_PURPLE = "#8b5cf6"
        ACCENT_PINK = "#ec4899"
        ACCENT_GREEN = "#059669"
        theme_btn.config(text="☀️ Light")
    
    # Update all widget colors
    root.config(bg=BG_PRIMARY)
    header_frame.config(bg=BG_SECONDARY)
    separator.config(bg=ACCENT_BLUE)
    search_section.config(bg=BG_SECONDARY)
    search_inner.config(bg=BG_SECONDARY)
    search_label.config(bg=BG_SECONDARY, fg=ACCENT_BLUE)
    entry.config(bg=BG_TERTIARY, fg=TEXT_PRIMARY)
    search_btn.config(bg=ACCENT_PINK)
    comp_btn.config(bg=ACCENT_PURPLE)
    status_label.config(bg=BG_SECONDARY, fg=TEXT_SECONDARY)
    main_frame.config(bg=BG_PRIMARY)
    history_panel.config(bg=BG_SECONDARY)
    history_frame.config(bg=BG_SECONDARY)
    content_frame.config(bg=BG_PRIMARY)
    canvas.config(bg=BG_PRIMARY)
    scrollbar.config(bg=BG_SECONDARY)
    scrollable_frame.config(bg=BG_PRIMARY)
    title_card.config(bg=BG_TERTIARY)
    title_label.config(bg=BG_TERTIARY, fg=ACCENT_BLUE)
    info_card.config(bg=BG_TERTIARY)
    year_label.config(bg=BG_TERTIARY, fg=ACCENT_PURPLE)
    genre_label.config(bg=BG_TERTIARY, fg=TEXT_SECONDARY)
    details_frame.config(bg=BG_PRIMARY)
    poster_frame.config(bg=BG_TERTIARY)
    poster_label.config(bg=BG_TERTIARY, fg=TEXT_SECONDARY)
    right_frame.config(bg=BG_PRIMARY)
    add_comp_btn.config(bg=ACCENT_GREEN)
    clear_comp_btn.config(bg=ACCENT_PINK)
    plot_text.config(bg=BG_TERTIARY, fg=TEXT_PRIMARY)
    
    update_history_buttons()
    load_logo()
    logo_label.config(bg=BG_SECONDARY)

BG_PRIMARY = "#0a0e27"
BG_SECONDARY = "#161b35"
BG_TERTIARY = "#1f2847"
TEXT_PRIMARY = "#e8f0ff"
TEXT_SECONDARY = "#a0b9d8"
ACCENT_BLUE = "#00d4ff"
ACCENT_PURPLE = "#bb86fc"
ACCENT_PINK = "#ff4081"
ACCENT_GREEN = "#00e676"

def search_movie():
    global current_movie_data
    
    movie_name = entry.get().strip()
    if not movie_name:
        messagebox.showwarning("Chyba", "Zadej název filmu!")
        return

    normalized_name = normalize_text(movie_name)
    status_label.config(text="🔍 Hledám...", fg=ACCENT_PURPLE)
    root.update()

    try:
        q = urllib.parse.quote_plus(normalized_name)
        url = f"https://www.omdbapi.com/?t={q}&apikey={API_KEY}"
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        status_label.config(text=f"❌ Chyba: {str(e)[:40]}", fg=ACCENT_PINK)
        return

    if data.get("Response") == "False":
        status_label.config(text="❌ Film/Seriál nebyl nalezen", fg=ACCENT_PINK)
        return

    current_movie_data = data
    title = data.get('Title', 'N/A')
    save_search_history(title)
    update_history_buttons()

    year = data.get('Year', 'N/A')
    genre = data.get('Genre', 'N/A')
    plot = data.get('Plot', 'N/A')
    rating = data.get('imdbRating', 'N/A')
    director = data.get('Director', 'N/A')
    actors = data.get('Actors', 'N/A')
    runtime = data.get('Runtime', 'N/A')
    movie_type = data.get('Type', 'N/A')
    country = data.get('Country', 'N/A')
    awards = data.get('Awards', 'N/A')
    rated = data.get('Rated', 'N/A')
    imdb_id = data.get('imdbID', '')
    
    if movie_type.lower() == 'series':
        total_seasons = data.get('totalSeasons', 'N/A')
        runtime_info = f"{runtime} za epizodu | {total_seasons} sezón"
    else:
        runtime_info = runtime

    title_var.set(title)
    year_var.set(f"{year} | Hodnocení: {rating}/10 | Typ: {movie_type}")
    genre_var.set(f"Žánr: {genre}")
    
    detailed_info = f"""• REŽISÉR: {director}

• HERCI: {actors}

• DOBA TRVÁNÍ: {runtime_info}

• ZEMĚ: {country}

• VĚKOVÁ KATEGORIE: {rated}

• OCENĚNÍ: {awards}

• IMDB ID: {imdb_id}

--- POPIS ---

{plot}"""
    plot_var.set(detailed_info)
    status_label.config(text="✓ Nalezeno!", fg=ACCENT_GREEN)

    poster_url = data.get("Poster")
    if poster_url and poster_url != "N/A":
        try:
            poster_response = requests.get(poster_url, timeout=8)
            poster_response.raise_for_status()
            img_data = poster_response.content
            img = Image.open(BytesIO(img_data)).convert("RGBA")
            img = img.resize((160, 240), Image.LANCZOS)
            poster_label.current_image = ImageTk.PhotoImage(img)
            poster_label.config(image=poster_label.current_image, text='', width=160, height=240, bg=BG_TERTIARY)
        except Exception:
            poster_label.config(image='', TEXT_PRIMARY="Bez\nplakátu", fg=TEXT_SECONDARY, width=20, height=12)
            poster_label.current_image = None
    else:
        poster_label.config(image='', text="Bez\nplakátu", fg=TEXT_SECONDARY, width=20, height=12)
        poster_label.current_image = None

def search_from_history(title):
    entry.delete(0, tk.END)
    entry.insert(0, title)
    search_movie()

def update_history_buttons():
    for widget in history_frame.winfo_children():
        widget.destroy()
    
    tk.Label(history_frame, text="📜 Historie:", font=("Segoe UI", 10, "bold"), fg=ACCENT_BLUE, bg=BG_SECONDARY).pack(anchor="w", padx=10, pady=(5, 5))
    
    for movie in search_history[:5]:
        btn = tk.Button(
            history_frame,
            text=f"• {movie[:25]}{'...' if len(movie) > 25 else ''}",
            font=("Segoe UI", 9),
            bg=BG_TERTIARY,
            fg=TEXT_PRIMARY,
            activebackground=ACCENT_BLUE,
            activeforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            anchor="w",
            command=lambda m=movie: search_from_history(m)
        )
        btn.pack(fill='x', padx=8, pady=2)

def add_to_comparison():
    global comparison_movies
    if not current_movie_data:
        messagebox.showwarning("Info", "Nejdřív si vyhledej film!")
        return
    
    title = current_movie_data.get('Title', 'N/A')
    if title not in [m.get('Title') for m in comparison_movies]:
        comparison_movies.append(current_movie_data)
        if len(comparison_movies) <= 3:
            messagebox.showinfo("✓ Přidáno", f"Film '{title}' přidán!\n({len(comparison_movies)}/3)")
            update_comparison_display()
        else:
            comparison_movies.pop()
            messagebox.showwarning("Limit", "Max 3 filmy!")
    else:
        messagebox.showinfo("Info", "Už v porovnání!")

def rating_to_percentage(rating_str):
    """Převede IMDB hodnocení na procenta"""
    try:
        rating = float(rating_str)
        return int((rating / 10) * 100)
    except:
        return 0

def get_rating_color(rating_str):
    """Vrátí barvu podle hodnocení"""
    try:
        rating = float(rating_str)
        if rating >= 8:
            return ACCENT_GREEN
        elif rating >= 7:
            return ACCENT_BLUE
        elif rating >= 6:
            return ACCENT_PURPLE
        else:
            return ACCENT_PINK
    except:
        return TEXT_SECONDARY

def show_comparison():
    if len(comparison_movies) == 0:
        messagebox.showinfo("Info", "Přidej alespoň 1 film!")
        return
    
    comp_window = tk.Toplevel(root)
    comp_window.title("⚖️ Porovnání filmů/seriálů")
    comp_window.geometry("1100x700")
    comp_window.configure(bg=BG_PRIMARY)
    
    comp_canvas = tk.Canvas(comp_window, bg=BG_PRIMARY, highlightthickness=0)
    comp_scrollbar = tk.Scrollbar(comp_window, orient="vertical", command=comp_canvas.yview)
    comp_frame = tk.Frame(comp_canvas, bg=BG_PRIMARY)
    
    comp_frame.bind("<Configure>", lambda e: comp_canvas.configure(scrollregion=comp_canvas.bbox("all")))
    comp_canvas.create_window((0, 0), window=comp_frame, anchor="nw")
    comp_canvas.configure(yscrollcommand=comp_scrollbar.set)
    
    comp_canvas.pack(side="left", fill="both", expand=True)
    comp_scrollbar.pack(side="right", fill="y")
    
    # Header
    header = tk.Frame(comp_frame, bg=BG_PRIMARY)
    header.pack(fill='x', padx=20, pady=20)
    tk.Label(header, text="⚖️ Porovnání", font=("Segoe UI", 18, "bold"), fg=ACCENT_BLUE, bg=BG_PRIMARY).pack(side='left')
    tk.Label(header, text=f"({len(comparison_movies)} film/seriál)", font=("Segoe UI", 11), fg=TEXT_SECONDARY, bg=BG_PRIMARY).pack(side='left', padx=(10, 0))
    
    # Sort by rating descending for better comparison
    sorted_movies = sorted(comparison_movies, key=lambda x: float(x.get('imdbRating', '0')), reverse=True)
    
    for idx, movie in enumerate(sorted_movies, 1):
        card = tk.Frame(comp_frame, bg=BG_TERTIARY, relief="flat", bd=1)
        card.pack(fill='x', padx=15, pady=12)
        
        title = movie.get('Title', 'N/A')
        year = movie.get('Year', 'N/A')
        rating_str = movie.get('imdbRating', 'N/A')
        percentage = rating_to_percentage(rating_str) if rating_str != 'N/A' else 0
        genre = movie.get('Genre', 'N/A')
        director = movie.get('Director', 'N/A')
        runtime = movie.get('Runtime', 'N/A')
        movie_type = movie.get('Type', 'N/A')
        poster_url = movie.get("Poster")
        
        # Main container for horizontal layout
        main_container = tk.Frame(card, bg=BG_TERTIARY)
        main_container.pack(fill='both', expand=True, padx=14, pady=14)
        
        # Left side - Poster
        poster_side = tk.Frame(main_container, bg=BG_SECONDARY, relief="flat", bd=0)
        poster_side.pack(side='left', padx=(0, 16), pady=0)
        
        poster_display = tk.Label(poster_side, bg=BG_SECONDARY, text="Bez\nplakátu", fg=TEXT_SECONDARY, font=("Segoe UI", 9), width=12, height=16)
        poster_display.pack()
        
        # Try to load poster image
        if poster_url and poster_url != "N/A":
            try:
                poster_response = requests.get(poster_url, timeout=5)
                poster_response.raise_for_status()
                img_data = poster_response.content
                img = Image.open(BytesIO(img_data)).convert("RGBA")
                img = img.resize((100, 150), Image.LANCZOS)
                poster_tk = ImageTk.PhotoImage(img)
                poster_display.config(image=poster_tk, text='', width=100, height=150, bg=BG_SECONDARY)
                poster_display.image = poster_tk
            except Exception:
                pass
        
        # Right side - Info
        info_side = tk.Frame(main_container, bg=BG_TERTIARY)
        info_side.pack(side='left', fill='both', expand=True)
        
        # Top section with title and year
        top_section = tk.Frame(info_side, bg=BG_TERTIARY)
        top_section.pack(fill='x', pady=(0, 10))
        
        tk.Label(top_section, text=f"{idx}. {title}", font=("Segoe UI", 13, "bold"), fg=ACCENT_BLUE, bg=BG_TERTIARY, wraplength=600, justify="left").pack(anchor="w")
        tk.Label(top_section, text=f"{year} • {movie_type.upper()} • {runtime}", font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_TERTIARY).pack(anchor="w", pady=(2, 0))
        
        # Rating section with progress bar
        rating_section = tk.Frame(info_side, bg=BG_TERTIARY)
        rating_section.pack(fill='x', pady=(0, 10))
        
        rating_color = get_rating_color(rating_str)
        
        # Rating display with percentage
        rating_label_frame = tk.Frame(rating_section, bg=BG_TERTIARY)
        rating_label_frame.pack(anchor="w")
        
        tk.Label(rating_label_frame, text="IMDb:", font=("Segoe UI", 10, "bold"), fg=TEXT_SECONDARY, bg=BG_TERTIARY).pack(side='left')
        tk.Label(rating_label_frame, text=f"  {rating_str}/10", font=("Segoe UI", 11, "bold"), fg=rating_color, bg=BG_TERTIARY).pack(side='left')
        tk.Label(rating_label_frame, text=f"  ({percentage}%)", font=("Segoe UI", 10), fg=rating_color, bg=BG_TERTIARY).pack(side='left', padx=(4, 0))
        
        # Visual progress bar
        progress_frame = tk.Frame(rating_section, bg=BG_SECONDARY, height=8)
        progress_frame.pack(fill='x', pady=(6, 0))
        
        if percentage > 0:
            bar_width = int(percentage * 3.5)  # Scale to fit
            bar = tk.Frame(progress_frame, bg=rating_color, height=8)
            bar.place(x=0, y=0, width=bar_width, height=8)
        
        # Info section
        info_section = tk.Frame(info_side, bg=BG_TERTIARY)
        info_section.pack(fill='x', pady=(0, 0))
        
        # Genre line
        genre_frame = tk.Frame(info_section, bg=BG_TERTIARY)
        genre_frame.pack(anchor="w")
        tk.Label(genre_frame, text="🎭", font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_TERTIARY).pack(side='left')
        tk.Label(genre_frame, text=genre, font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_TERTIARY, justify="left").pack(side='left', anchor="w")
        
        # Director line
        director_frame = tk.Frame(info_section, bg=BG_TERTIARY)
        director_frame.pack(anchor="w", pady=(2, 0))
        tk.Label(director_frame, text="📽️", font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_TERTIARY).pack(side='left')
        tk.Label(director_frame, text=f"Režie: {director}", font=("Segoe UI", 9), fg=TEXT_SECONDARY, bg=BG_TERTIARY, justify="left").pack(side='left', anchor="w")

def clear_comparison():
    global comparison_movies
    comparison_movies = []
    update_comparison_display()
    messagebox.showinfo("✓", "Porovnání vymazáno!")

def update_comparison_display():
    count = len(comparison_movies)
    comp_btn.config(text=f"⚖️ Porovnání ({count}/3)")

root = tk.Tk()
root.title("🎬 MovieExplorer")
root.configure(bg=BG_PRIMARY)
root.geometry("1500x900")
root.minsize(1100, 750)

load_search_history()

root_dir = Path(__file__).resolve().parent
logo_path = root_dir / "logo.png"
logo2_path = root_dir / "logo2.png"
logo_tk = None

def load_logo():
    """Load appropriate logo based on dark_mode"""
    global logo_tk
    try:
        if dark_mode:
            path = logo_path
        else:
            path = logo2_path
        
        if path.exists():
            logo = Image.open(path).convert("RGBA")
            logo = logo.resize((420, 100), Image.LANCZOS)
            logo_tk = ImageTk.PhotoImage(logo)
            if logo_label:
                logo_label.config(image=logo_tk)
    except:
        pass

header_frame = tk.Frame(root, bg=BG_SECONDARY, height=120)
header_frame.pack(fill='x', pady=0)
header_frame.pack_propagate(False)

separator = tk.Frame(header_frame, bg=ACCENT_BLUE, height=2)
separator.pack(side='bottom', fill='x')

logo_label = tk.Label(header_frame, bg=BG_SECONDARY)
logo_label.pack(side='left', padx=24, pady=12)

load_logo()

theme_btn = tk.Button(header_frame, text="🌙 Dark", font=("Segoe UI", 10, "bold"), bg=ACCENT_PURPLE, fg="white", activebackground="#9d6ddb", relief="flat", bd=0, padx=12, pady=8, highlightthickness=0, highlightcolor=ACCENT_PURPLE, highlightbackground=ACCENT_PURPLE, command=toggle_dark_mode)
theme_btn.pack(side='right', padx=24, pady=12)

search_section = tk.Frame(root, bg=BG_SECONDARY, height=100)
search_section.pack(fill='x', padx=0, pady=0)
search_section.pack_propagate(False)

search_inner = tk.Frame(search_section, bg=BG_SECONDARY)
search_inner.pack(fill='both', expand=True, padx=28, pady=16)

search_label = tk.Label(search_inner, text="🔎 Vyhledej film nebo seriál", font=("Segoe UI", 14, "bold"), fg=ACCENT_BLUE, bg=BG_SECONDARY)
search_label.pack(anchor="w", pady=(0, 12))

entry_frame = tk.Frame(search_inner, bg=BG_SECONDARY)
entry_frame.pack(fill='x', pady=0)

entry = tk.Entry(entry_frame, width=60, font=("Segoe UI", 13), bg=BG_TERTIARY, fg=TEXT_PRIMARY, insertbackground=ACCENT_BLUE, relief="flat", bd=0, highlightthickness=0)
entry.pack(side='left', fill='x', expand=True, ipady=12)
entry.bind('<Return>', lambda e: search_movie())

search_btn = tk.Button(entry_frame, text="🔍 Hledej", font=("Segoe UI", 12, "bold"), bg=ACCENT_PINK, fg="white", activebackground="#e61e63", relief="flat", bd=0, padx=28, pady=12, highlightthickness=0, highlightcolor=ACCENT_PINK, highlightbackground=ACCENT_PINK, command=search_movie)
search_btn.pack(side='left', padx=(14, 0))

comp_btn = tk.Button(entry_frame, text="⚖️ Porovnání (0/3)", font=("Segoe UI", 11, "bold"), bg=ACCENT_PURPLE, fg="white", activebackground="#9d6ddb", relief="flat", bd=0, padx=16, pady=12, highlightthickness=0, highlightcolor=ACCENT_PURPLE, highlightbackground=ACCENT_PURPLE, command=show_comparison)
comp_btn.pack(side='left', padx=(8, 0))

status_label = tk.Label(search_inner, text="Začni psaním...", font=("Segoe UI", 10), fg=TEXT_SECONDARY, bg=BG_SECONDARY)
status_label.pack(anchor="w", pady=(12, 0))

main_frame = tk.Frame(root, bg=BG_PRIMARY)
main_frame.pack(fill='both', expand=True, padx=28, pady=20)

history_panel = tk.Frame(main_frame, bg=BG_SECONDARY, width=180)
history_panel.pack(side='left', fill='y', padx=(0, 20))
history_panel.pack_propagate(False)

history_frame = tk.Frame(history_panel, bg=BG_SECONDARY)
history_frame.pack(fill='both', expand=True, padx=0, pady=10)

update_history_buttons()

content_frame = tk.Frame(main_frame, bg=BG_PRIMARY)
content_frame.pack(side='left', fill='both', expand=True)

canvas = tk.Canvas(content_frame, bg=BG_PRIMARY, highlightthickness=0)
scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview, bg=BG_SECONDARY, activebackground=ACCENT_BLUE, width=14)
scrollable_frame = tk.Frame(canvas, bg=BG_PRIMARY)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

title_card = tk.Frame(scrollable_frame, bg=BG_TERTIARY)
title_card.pack(fill='x', pady=(0, 18))

title_var = tk.StringVar()
title_label = tk.Label(title_card, textvariable=title_var, font=("Segoe UI", 26, "bold"), fg=ACCENT_BLUE, bg=BG_TERTIARY, wraplength=1100, justify="left")
title_label.pack(anchor="w", padx=18, pady=16)

info_card = tk.Frame(scrollable_frame, bg=BG_TERTIARY)
info_card.pack(fill='x', pady=(0, 18))

year_var = tk.StringVar()
year_label = tk.Label(info_card, textvariable=year_var, font=("Segoe UI", 12), fg=ACCENT_PURPLE, bg=BG_TERTIARY)
year_label.pack(anchor="w", padx=18, pady=(12, 4))

genre_var = tk.StringVar()
genre_label = tk.Label(info_card, textvariable=genre_var, font=("Segoe UI", 11), fg=TEXT_SECONDARY, bg=BG_TERTIARY, wraplength=1100, justify="left")
genre_label.pack(anchor="w", padx=18, pady=(0, 12))

details_frame = tk.Frame(scrollable_frame, bg=BG_PRIMARY)
details_frame.pack(fill='both', expand=True, pady=(0, 24))

poster_frame = tk.Frame(details_frame, bg=BG_TERTIARY)
poster_frame.pack(side='left', padx=(0, 24), pady=0)

poster_label = tk.Label(poster_frame, bg=BG_TERTIARY, text="Bez\nplakátu", fg=TEXT_SECONDARY, font=("Segoe UI", 11), width=20, height=14)
poster_label.pack(padx=14, pady=14)
poster_label.current_image = None

right_frame = tk.Frame(details_frame, bg=BG_PRIMARY)
right_frame.pack(side='left', fill='both', expand=True)

add_comp_btn = tk.Button(right_frame, text="⭐ Přidat k porovnání", font=("Segoe UI", 10, "bold"), bg=ACCENT_GREEN, fg="white", activebackground="#00cc55", relief="flat", bd=0, padx=12, pady=8, highlightthickness=0, highlightcolor=ACCENT_GREEN, highlightbackground=ACCENT_GREEN, command=add_to_comparison)
add_comp_btn.pack(anchor="w", pady=(0, 10))

clear_comp_btn = tk.Button(right_frame, text="🗑️ Vymazat porovnání", font=("Segoe UI", 9), bg=ACCENT_PINK, fg="white", activebackground="#e61e63", relief="flat", bd=0, padx=12, pady=6, highlightthickness=0, highlightcolor=ACCENT_PINK, highlightbackground=ACCENT_PINK, command=clear_comparison)
clear_comp_btn.pack(anchor="w", pady=(0, 12))

plot_var = tk.StringVar()
plot_text = scrolledtext.ScrolledText(right_frame, width=92, height=26, font=("Segoe UI", 11), fg=TEXT_PRIMARY, bg=BG_TERTIARY, wrap='word', relief="flat", bd=0)
plot_text.pack(fill='both', expand=True)
plot_text.config(state='disabled')

def update_plot(text):
    plot_text.config(state='normal')
    plot_text.delete('1.0', 'end')
    plot_text.insert('1.0', text)
    plot_text.config(state='disabled')

plot_var.trace('w', lambda *args: update_plot(plot_var.get()))

root.mainloop()
