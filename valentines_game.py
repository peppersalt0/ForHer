#!/usr/bin/env python3

import tkinter as tk
from tkinter import font as tkfont
import random
import math
import time
import os

try:
    import pygame
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except:
    AUDIO_AVAILABLE = False

def start_music():
    if AUDIO_AVAILABLE:
        try:
            music_path = os.path.join(os.path.dirname(__file__), 'assets', 'music.mp3')
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
        except:
            pass

CELEBRATION_TEXT = "See you on Feb 14 at 11:30 ❤️"
WINDOW_TITLE = "Word Hunt 💕"

COLORS = {
    'background': '#FFFAF5',
    'grid_bg': '#FFFFFF',
    'cell_normal': '#FFFFFF',
    'cell_selected': '#F8BBD9',
    'cell_path': '#FDDDE6',
    'text_dark': '#4A4A4A',
    'text_light': '#FFFFFF',
    'main_word': '#E991B4',
    'bonus_word': '#D4A5A5',
    'button_yes': '#FDDDE6',
    'button_no': '#F5F5F5',
    'timer': '#E8A0A0',
    'celebration_bg': '#FFFAF5',
}

GAME_DURATION = 60
MAIN_WORD_POINTS = 1_000_000
BONUS_WORD_POINTS = 100

GRID = [
    ['V', 'A', 'L', 'B'],
    ['E', 'N', 'L', 'E'],
    ['W', 'I', 'T', 'N'],
    ['M', 'Y', 'O', 'U']
]

MAIN_WORDS = {'will', 'you', 'be', 'my', 'valentine'}
MAIN_WORDS_ORDERED = ['will', 'you', 'be', 'my', 'valentine']

def load_dictionary():
    words = set()
    dict_paths = [
        os.path.join(os.path.dirname(__file__), 'words.txt'),
        os.path.join(os.path.dirname(__file__), 'dictionary.txt'),
        '/usr/share/dict/words',
    ]
    for path in dict_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        word = line.strip().lower()
                        if 2 <= len(word) <= 16:
                            words.add(word)
                if words:
                    break
            except Exception as e:
                pass
    words.update(MAIN_WORDS)
    valid_grid_words = {
        'valentine', 'antlion', 'outline', 'alvenal', 'unline', 'valine', 'vanity', 'veinal', 'venite', 'ventil',
        'willet', 'wintle', 'online', 'outlie', 'untile', 'alien', 'aline', 'anile', 'anion', 'belie', 'bento', 'benty',
        'beton', 'blent', 'blimy', 'blite', 'elint', 'enlit', 'inlet', 'intel', 'lenti', 'lento', 'linty', 'mille', 'milty', 'minae',
        'minty', 'niton', 'noint', 'outie', 'telae', 'tinea', 'toile', 'unlet', 'unlit', 'untie', 'until', 'unity', 'utile', 'valet',
        'venal', 'aliyot', 'lentil', 'lienal', 'lineal', 'lionel', 'lionet', 'millet', 'milneb', 'nellie', 'oillet', 'oilnut',
        'tellin', 'tineal', 'albe', 'alit', 'alto', 'anew', 'anil', 'ante', 'anti', 'bell', 'belt', 'bent', 'blae', 'blet', 'blin',
        'eale', 'eina', 'elan', 'etna', 'into', 'lane', 'lant', 'lave', 'leno', 'lent', 'lien', 'limy', 'line', 'lint', 'lion', 'lite',
        'litu', 'mien', 'mile', 'mill', 'milt', 'mina', 'mine', 'mint', 'mite', 'mity', 'nave', 'neal', 'nill', 'nite', 'noil', 'note',
        'nout', 'oint', 'tela', 'tell', 'tile', 'till', 'tina', 'tine', 'toil', 'tone', 'toun', 'tune', 'tyin', 'unto', 'vale', 'vali',
        'vane', 'vant', 'veal', 'veil', 'vein', 'vena', 'vent', 'weal', 'wean', 'weil', 'wena', 'went', 'wile', 'will', 'wilt', 'wine',
        'wite', 'wyte', 'yill', 'yite', 'yont', 'yote', 'alb', 'ale', 'all', 'alt', 'ane', 'ani', 'ant', 'ave', 'bel', 'ben', 'bet',
        'ean', 'ell', 'elt', 'ill', 'int', 'ion', 'lav', 'lea', 'let', 'leu', 'lie', 'lin', 'lit', 'mil', 'nae', 'nav', 'neb', 'net',
        'new', 'nie', 'nil', 'nim', 'nit', 'not', 'noy', 'nut', 'oil', 'one', 'out', 'tel', 'ten', 'tie', 'til', 'tin', 'ton', 'toy',
        'tui', 'tun', 'ute', 'vae', 'van', 'vat', 'vet', 'vie', 'wen', 'wet', 'win', 'wit', 'wot', 'yin', 'yon', 'you',
        'al', 'an', 'be', 'el', 'en', 'in', 'it', 'la', 'li', 'lo', 'mi', 'my', 'na', 'ne', 'no', 'nu', 'oi', 'on', 'ou', 'oy',
        'ta', 'te', 'ti', 'to', 'un', 'ut', 'we', 'ye', 'yo',
    }
    words.update(valid_grid_words)
    return words

class AnimatedGIF:
    def __init__(self, parent, gif_path, bg_color='white', max_size=(300, 300)):
        try:
            from PIL import Image, ImageTk
        except ImportError:
            print("Pillow not installed. Run: pip3 install Pillow")
            return
        self.parent = parent
        self.bg_color = bg_color
        self.frames = []
        self.frame_index = 0
        self.is_running = True
        gif = Image.open(gif_path)
        gif.thumbnail(max_size, Image.Resampling.LANCZOS)
        try:
            while True:
                frame = gif.copy()
                if frame.mode != 'RGBA':
                    frame = frame.convert('RGBA')
                self.frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(self.frames))
        except EOFError:
            pass
        self.label = tk.Label(parent, bg=bg_color)
        try:
            self.delay = gif.info.get('duration', 100)
        except:
            self.delay = 100
        if self.delay < 20:
            self.delay = 100
        self.animate()

    def animate(self):
        if not self.is_running or not self.frames:
            return
        self.label.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.parent.after(self.delay, self.animate)

    def stop(self):
        self.is_running = False

class ValentinesWordHunt:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg=COLORS['background'])
        self.root.geometry("1920x1080")
        self.root.resizable(True, True)
        self.dictionary = load_dictionary()
        self.found_main_words = set()
        self.found_bonus_words = set()
        self.score = 0
        self.time_left = GAME_DURATION
        self.game_active = False
        self.timer_id = None
        self.selected_cells = []
        self.current_word = ""
        self.is_dragging = False
        self.drag_origin_x = 0
        self.drag_origin_y = 0
        self.last_selection_time = 0
        self.cell_buttons = []
        self.cell_frames = []
        self.setup_ui()
        self.show_start_screen()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=COLORS['background'])
        self.main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        self.top_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        self.top_frame.pack(fill='x', pady=(0, 15))
        self.score_label = tk.Label(
            self.top_frame, text="Score: 0", font=('Helvetica', 32, 'bold'),
            bg=COLORS['background'], fg=COLORS['text_dark']
        )
        self.score_label.pack(side='left')
        self.timer_label = tk.Label(
            self.top_frame, text=f"⏱️ {GAME_DURATION}", font=('Helvetica', 32, 'bold'),
            bg=COLORS['background'], fg=COLORS['timer']
        )
        self.timer_label.pack(side='right')
        self.word_display = tk.Label(
            self.main_frame, text="", font=('Helvetica', 38, 'bold'),
            bg=COLORS['background'], fg=COLORS['main_word'], height=1
        )
        self.word_display.pack(pady=(0, 10))
        self.content_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        self.content_frame.pack(expand=True)
        self.grid_container = tk.Frame(self.content_frame, bg='#FFF5F8', padx=15, pady=15)
        self.grid_container.pack(side='left', padx=(0, 50))
        self.grid_frame = tk.Frame(self.grid_container, bg='#FFF5F8')
        self.grid_frame.pack()
        self.create_grid()
        self.banks_frame = tk.Frame(self.content_frame, bg=COLORS['background'], width=350)
        self.banks_frame.pack(side='left', fill='y')
        self.banks_frame.pack_propagate(False)
        main_bank_label = tk.Label(
            self.banks_frame, text="💕 Special Words", font=('Helvetica', 22, 'bold'),
            bg=COLORS['background'], fg=COLORS['main_word']
        )
        main_bank_label.pack(anchor='w')
        self.main_words_frame = tk.Frame(self.banks_frame, bg=COLORS['background'])
        self.main_words_frame.pack(fill='x', pady=(8, 20))
        self.main_word_labels = {}
        for word in MAIN_WORDS_ORDERED:
            label = tk.Label(
                self.main_words_frame, text="_ " * len(word), font=('Helvetica', 20),
                bg=COLORS['background'], fg=COLORS['text_dark']
            )
            label.pack(anchor='w', pady=1)
            self.main_word_labels[word] = label
        bonus_bank_label = tk.Label(
            self.banks_frame, text="⭐ Bonus Words", font=('Helvetica', 22, 'bold'),
            bg=COLORS['background'], fg=COLORS['bonus_word']
        )
        bonus_bank_label.pack(anchor='w', pady=(20, 0))
        self.bonus_words_text = tk.Text(
            self.banks_frame, font=('Helvetica', 14), bg='#FFF5F8', fg=COLORS['bonus_word'],
            width=22, height=12, state='disabled', wrap='word', relief='flat',
            highlightthickness=1, highlightbackground='#E0E0E0'
        )
        self.bonus_words_text.pack(fill='x', pady=8)

    def create_grid(self):
        cell_size = 120
        for row in range(4):
            row_frames = []
            row_buttons = []
            for col in range(4):
                frame = tk.Frame(
                    self.grid_frame, width=cell_size, height=cell_size, bg=COLORS['cell_normal'],
                    highlightbackground='#E0E0E0', highlightthickness=2
                )
                frame.grid(row=row, column=col, padx=4, pady=4)
                frame.pack_propagate(False)
                label = tk.Label(
                    frame, text=GRID[row][col], font=('Helvetica', 48, 'bold'),
                    bg=COLORS['cell_normal'], fg=COLORS['text_dark']
                )
                label.pack(expand=True)
                for widget in [frame, label]:
                    widget.bind('<Button-1>', lambda e, r=row, c=col: self.on_cell_press(r, c))
                    widget.bind('<B1-Motion>', lambda e, r=row, c=col: self.on_cell_drag(e, r, c))
                    widget.bind('<ButtonRelease-1>', lambda e: self.on_release())
                    widget.bind('<Enter>', lambda e, r=row, c=col: self.on_cell_enter(r, c))
                row_frames.append(frame)
                row_buttons.append(label)
            self.cell_frames.append(row_frames)
            self.cell_buttons.append(row_buttons)

    def on_cell_press(self, row, col):
        if not self.game_active:
            return
        self.is_dragging = True
        self.selected_cells = [(row, col)]
        self.current_word = GRID[row][col]
        self.update_selection_display()
        frame = self.cell_frames[row][col]
        self.drag_origin_x = frame.winfo_rootx() + frame.winfo_width() // 2
        self.drag_origin_y = frame.winfo_rooty() + frame.winfo_height() // 2
        self.last_selection_time = time.time()

    def on_cell_enter(self, row, col):
        pass

    def on_cell_drag(self, event, orig_row, orig_col):
        if not self.is_dragging or not self.game_active or not self.selected_cells:
            return
        if time.time() - self.last_selection_time < 0.1:
            return
        last_row, last_col = self.selected_cells[-1]
        last_frame = self.cell_frames[last_row][last_col]
        mouse_x = event.x_root
        mouse_y = event.y_root
        dx = mouse_x - self.drag_origin_x
        dy = mouse_y - self.drag_origin_y
        cell_size = last_frame.winfo_width()
        min_distance = cell_size * 0.85
        distance = (dx**2 + dy**2) ** 0.5
        if distance < min_distance:
            return
        angle = math.atan2(dy, dx) * 180 / math.pi
        directions = [
            (0, 1, 0, 30), (1, 1, 45, 35), (1, 0, 90, 30), (1, -1, 135, 35),
            (0, -1, 180, 30), (-1, -1, -135, 35), (-1, 0, -90, 30), (-1, 1, -45, 35),
        ]
        best_match = None
        best_score = float('inf')
        for row_off, col_off, center_angle, half_width in directions:
            new_row = last_row + row_off
            new_col = last_col + col_off
            if not (0 <= new_row < 4 and 0 <= new_col < 4):
                continue
            if (new_row, new_col) in self.selected_cells:
                continue
            angle_diff = abs(angle - center_angle)
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            is_diagonal = row_off != 0 and col_off != 0
            effective_half_width = half_width + (10 if is_diagonal else 0)
            if angle_diff <= effective_half_width:
                score = angle_diff
                if is_diagonal:
                    score -= 5
                if score < best_score:
                    best_score = score
                    best_match = (new_row, new_col)
        if best_match:
            new_row, new_col = best_match
            self.selected_cells.append((new_row, new_col))
            self.current_word += GRID[new_row][new_col]
            self.update_selection_display()
            new_frame = self.cell_frames[new_row][new_col]
            self.drag_origin_x = new_frame.winfo_rootx() + new_frame.winfo_width() // 2
            self.drag_origin_y = new_frame.winfo_rooty() + new_frame.winfo_height() // 2
            self.last_selection_time = time.time()

    def on_release(self):
        if not self.game_active:
            return
        self.is_dragging = False
        word = self.current_word.lower()
        if len(word) >= 2 and word in self.dictionary:
            if word in MAIN_WORDS and word not in self.found_main_words:
                self.found_main_words.add(word)
                self.score += MAIN_WORD_POINTS
                self.update_main_word_display(word)
                self.flash_cells(COLORS['main_word'])
            elif word not in MAIN_WORDS and word not in self.found_bonus_words:
                self.found_bonus_words.add(word)
                self.score += BONUS_WORD_POINTS
                self.update_bonus_word_display(word)
                self.flash_cells(COLORS['bonus_word'])
            self.score_label.config(text=f"Score: {self.score:,}")
        self.selected_cells = []
        self.current_word = ""
        self.update_selection_display()

    def update_selection_display(self):
        for row in range(4):
            for col in range(4):
                self.cell_frames[row][col].config(bg=COLORS['cell_normal'])
                self.cell_buttons[row][col].config(bg=COLORS['cell_normal'])
        for i, (row, col) in enumerate(self.selected_cells):
            color = COLORS['cell_selected'] if i == len(self.selected_cells) - 1 else COLORS['cell_path']
            self.cell_frames[row][col].config(bg=color)
            self.cell_buttons[row][col].config(bg=color)
        self.word_display.config(text=self.current_word.upper())

    def flash_cells(self, color):
        for row, col in self.selected_cells:
            self.cell_frames[row][col].config(bg=color)
            self.cell_buttons[row][col].config(bg=color)
        self.root.after(200, self.update_selection_display)

    def update_main_word_display(self, word):
        if word in self.main_word_labels:
            self.main_word_labels[word].config(
                text=word.upper(), fg=COLORS['main_word'], font=('Helvetica', 20, 'bold')
            )

    def update_bonus_word_display(self, word):
        self.bonus_words_text.config(state='normal')
        self.bonus_words_text.insert('end', word.upper() + " +100\n")
        self.bonus_words_text.config(state='disabled')
        self.bonus_words_text.see('end')

    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"⏱️ {self.time_left}")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.start_timer)
        else:
            self.end_game()

    def end_game(self):
        self.game_active = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        all_found = self.found_main_words == MAIN_WORDS
        self.show_end_screen(all_found)

    def show_start_screen(self):
        self.overlay = tk.Frame(self.root, bg=COLORS['background'])
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        title = tk.Label(
            self.overlay, text="💕 Word Hunt 💕", font=('Helvetica', 72, 'bold'),
            bg=COLORS['background'], fg=COLORS['main_word']
        )
        title.pack(pady=(200, 30))
        subtitle = tk.Label(
            self.overlay, text="Find all the hidden words!", font=('Helvetica', 32),
            bg=COLORS['background'], fg=COLORS['text_dark']
        )
        subtitle.pack(pady=20)
        instructions = tk.Label(
            self.overlay, text="Drag through letters to form words.\nThere's a special message hidden in the grid!",
            font=('Helvetica', 22), bg=COLORS['background'], fg=COLORS['text_dark'], justify='center'
        )
        instructions.pack(pady=30)
        start_btn = tk.Button(
            self.overlay, text="Start Game", font=('Helvetica', 36, 'bold'),
            bg=COLORS['button_yes'], fg=COLORS['text_dark'], padx=60, pady=25,
            command=self.start_game, cursor='hand2'
        )
        start_btn.pack(pady=60)

    def start_game(self):
        self.overlay.destroy()
        self.game_active = True
        start_music()
        self.start_timer()

    def show_end_screen(self, success):
        self.overlay = tk.Frame(self.root, bg=COLORS['background'])
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        if success:
            title = tk.Label(
                self.overlay, text="You found the message!", font=('Helvetica', 48, 'bold'),
                bg=COLORS['background'], fg=COLORS['main_word']
            )
            title.pack(pady=(150, 30))
            message = tk.Label(
                self.overlay, text="Will You Be My Valentine?", font=('Helvetica', 64, 'bold'),
                bg=COLORS['background'], fg=COLORS['text_dark']
            )
            message.pack(pady=50)
            btn_frame = tk.Frame(self.overlay, bg=COLORS['background'])
            btn_frame.pack(pady=60)
            yes_btn = tk.Button(
                btn_frame, text="Yes! 💕", font=('Helvetica', 36, 'bold'),
                bg=COLORS['button_yes'], fg=COLORS['text_dark'], padx=60, pady=25,
                command=self.show_celebration, cursor='hand2'
            )
            yes_btn.pack(side='left', padx=30)
            self.no_btn = tk.Button(
                btn_frame, text="No", font=('Helvetica', 36, 'bold'),
                bg=COLORS['button_no'], fg=COLORS['text_dark'], padx=60, pady=25, cursor='hand2'
            )
            self.no_btn.pack(side='left', padx=30)
            self.no_escape_count = 0
            self.no_btn.bind('<Enter>', self.escape_no_button)
        else:
            title = tk.Label(
                self.overlay, text="Time's Up!", font=('Helvetica', 48, 'bold'),
                bg=COLORS['background'], fg=COLORS['timer']
            )
            title.pack(pady=(150, 30))
            found_text = f"You found {len(self.found_main_words)}/{len(MAIN_WORDS)} special words"
            found_label = tk.Label(
                self.overlay, text=found_text, font=('Helvetica', 32),
                bg=COLORS['background'], fg=COLORS['text_dark']
            )
            found_label.pack(pady=30)
            hint = tk.Label(
                self.overlay, text="There's a hidden message in the grid...\nKeep looking!",
                font=('Helvetica', 22), bg=COLORS['background'], fg=COLORS['bonus_word'], justify='center'
            )
            hint.pack(pady=30)
            retry_btn = tk.Button(
                self.overlay, text="Try Again?", font=('Helvetica', 36, 'bold'),
                bg=COLORS['button_yes'], fg=COLORS['text_dark'], padx=60, pady=25,
                command=self.restart_game, cursor='hand2'
            )
            retry_btn.pack(pady=60)

    def escape_no_button(self, event):
        self.no_escape_count += 1
        if self.no_escape_count >= 7:
            self.no_btn.destroy()
            return
        if self.no_escape_count == 1:
            self.overlay.update_idletasks()
            for widget in self.overlay.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and "Yes" in child.cget("text"):
                            self.yes_btn_x = child.winfo_rootx() - self.overlay.winfo_rootx()
                            self.yes_btn_y = child.winfo_rooty() - self.overlay.winfo_rooty()
                            self.yes_btn_width = child.winfo_width()
                            self.yes_btn_height = child.winfo_height()
                            break
            old_btn = self.no_btn
            self.no_btn = tk.Button(
                self.overlay, text="No", font=('Helvetica', 36, 'bold'),
                bg=COLORS['button_no'], fg=COLORS['text_dark'], padx=60, pady=25, cursor='hand2'
            )
            self.no_btn.bind('<Enter>', self.escape_no_button)
            old_btn.destroy()
        self.overlay.update_idletasks()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        btn_width = 200
        btn_height = 90
        padding = 80
        min_x = padding
        max_x = window_width - btn_width - padding
        min_y = padding
        max_y = window_height - btn_height - padding
        if max_x <= min_x:
            max_x = min_x + 50
        if max_y <= min_y:
            max_y = min_y + 50
        mouse_x = event.x_root - self.overlay.winfo_rootx()
        mouse_y = event.y_root - self.overlay.winfo_rooty()
        for _ in range(50):
            new_x = random.randint(min_x, max_x)
            new_y = random.randint(min_y, max_y)
            dist_from_mouse = ((new_x - mouse_x)**2 + (new_y - mouse_y)**2)**0.5
            yes_padding = 50
            overlaps_yes = (
                hasattr(self, 'yes_btn_x') and
                new_x < self.yes_btn_x + self.yes_btn_width + yes_padding and
                new_x + btn_width > self.yes_btn_x - yes_padding and
                new_y < self.yes_btn_y + self.yes_btn_height + yes_padding and
                new_y + btn_height > self.yes_btn_y - yes_padding
            )
            if dist_from_mouse > 200 and not overlaps_yes:
                break
        self.no_btn.place(x=new_x, y=new_y)

    def show_celebration(self):
        for widget in self.overlay.winfo_children():
            widget.destroy()
        self.overlay.config(bg=COLORS['celebration_bg'])
        self.celebration_images = []
        self.celebration_gifs = []
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')
        
        yay = tk.Label(
            self.overlay, text="Yay!!!", font=('Helvetica', 72, 'bold'),
            bg=COLORS['celebration_bg'], fg=COLORS['main_word']
        )
        yay.place(x=720, y=300, anchor='n')
        
        message = tk.Label(
            self.overlay, text=CELEBRATION_TEXT, font=('Helvetica', 30),
            bg=COLORS['celebration_bg'], fg=COLORS['text_dark'], justify='center'
        )
        message.place(x=750, y=430, anchor='n')
        
        try:
            from PIL import Image, ImageTk
            img = Image.open(os.path.join(assets_path, 'tulip.png'))
            img.thumbnail((220, 220))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
            img_label.image = photo
            self.celebration_images.append(photo)
            img_label.place(x=80, y=370)
        except Exception as e:
            print(f"Could not load tulip: {e}")
        
        try:
            from PIL import Image, ImageTk
            img = Image.open(os.path.join(assets_path, 'otterpuppy.JPG'))
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
            img_label.image = photo
            self.celebration_images.append(photo)
            img_label.place(x=200, y=650)
        except Exception as e:
            print(f"Could not load otter: {e}")
        
        try:
            from PIL import Image, ImageTk
            img = Image.open(os.path.join(assets_path, 'hamster.png'))
            img.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
            img_label.image = photo
            self.celebration_images.append(photo)
            img_label.place(x=550, y=40)
        except Exception as e:
            print(f"Could not load hamster: {e}")
        
        try:
            from PIL import Image, ImageTk
            img = Image.open(os.path.join(assets_path, 'dubai.jpg'))
            img.thumbnail((180, 180))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
            img_label.image = photo
            self.celebration_images.append(photo)
            img_label.place(x=820, y=70)
        except Exception as e:
            print(f"Could not load dubai: {e}")
        
        try:
            from PIL import Image, ImageTk
            img = Image.open(os.path.join(assets_path, 'stingray.jpg'))
            img.thumbnail((200, 150))
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
            img_label.image = photo
            self.celebration_images.append(photo)
            img_label.place(x=300, y=220)
        except Exception as e:
            print(f"Could not load stingray: {e}")
        
        try:
            gif = AnimatedGIF(
                self.overlay, os.path.join(assets_path, 'dog.gif'),
                bg_color=COLORS['celebration_bg'], max_size=(180, 180)
            )
            gif.label.place(x=80, y=80)
            self.celebration_gifs.append(gif)
        except Exception as e:
            print(f"Could not load dog gif: {e}")
        
        try:
            gif = AnimatedGIF(
                self.overlay, os.path.join(assets_path, 'yoda.gif'),
                bg_color=COLORS['celebration_bg']
            )
            gif.label.place(x=1000, y=80)
            self.celebration_gifs.append(gif)
        except Exception as e:
            print(f"Could not load yoda gif: {e}")
        
        try:
            gif = AnimatedGIF(
                self.overlay, os.path.join(assets_path, 'wolf.gif'),
                bg_color=COLORS['celebration_bg'], max_size=(160, 200)
            )
            gif.label.place(x=550, y=600)
            self.celebration_gifs.append(gif)
        except Exception as e:
            print(f"Could not load wolf gif: {e}")
        
        try:
            gif = AnimatedGIF(
                self.overlay, os.path.join(assets_path, 'cat_yipe.gif'),
                bg_color=COLORS['celebration_bg']
            )
            gif.label.place(x=860, y=620)
            self.celebration_gifs.append(gif)
        except Exception as e:
            print(f"Could not load cat gif: {e}")
        
        try:
            gif = AnimatedGIF(
                self.overlay, os.path.join(assets_path, 'hadilao.gif'),
                bg_color=COLORS['celebration_bg']
            )
            gif.label.place(x=1200, y=400)
            self.celebration_gifs.append(gif)
        except Exception as e:
            print(f"Could not load hadilao gif: {e}")

    def restart_game(self):
        self.overlay.destroy()
        self.found_main_words = set()
        self.found_bonus_words = set()
        self.score = 0
        self.time_left = GAME_DURATION
        self.selected_cells = []
        self.current_word = ""
        self.score_label.config(text="Score: 0")
        self.timer_label.config(text=f"⏱️ {GAME_DURATION}")
        self.word_display.config(text="")
        for word, label in self.main_word_labels.items():
            label.config(text="_ " * len(word), fg=COLORS['text_dark'], font=('Helvetica', 20))
        self.bonus_words_text.config(state='normal')
        self.bonus_words_text.delete('1.0', 'end')
        self.bonus_words_text.config(state='disabled')
        self.update_selection_display()
        self.game_active = True
        self.start_timer()

if __name__ == "__main__":
    root = tk.Tk()
    game = ValentinesWordHunt(root)
    root.mainloop()