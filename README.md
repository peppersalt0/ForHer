# 💕 Valentine's Word Hunt 💕

A cute word hunt game to ask someone special to be your Valentine!

## How It Works

1. The game presents a 4x4 grid of letters
2. Players drag through letters to form words
3. Hidden in the grid are the words: **WILL**, **YOU**, **BE**, **MY**, **VALENTINE**
4. Finding all 5 special words reveals the question: "Will You Be My Valentine?"
5. If they click "No"... the button runs away! 😄
6. If they click "Yes"... celebration time! 🎉

---

## 🚀 Running on Mac (No IDE Needed!)

### Method 1: Double-Click (Easiest)

1. Open **Terminal** (press `Cmd + Space`, type "Terminal", press Enter)
2. Navigate to the game folder:
   ```bash
   cd /path/to/valentines_word_hunt
   ```
3. Make the game executable:
   ```bash
   chmod +x valentines_game.py
   ```
4. Now you can double-click `valentines_game.py` in Finder!
   - If it opens in a text editor instead, right-click → Open With → Python Launcher

### Method 2: Run from Terminal

1. Open **Terminal**
2. Navigate to the game folder:
   ```bash
   cd /path/to/valentines_word_hunt
   ```
3. Run the game:
   ```bash
   python3 valentines_game.py
   ```

### Method 3: Create a Clickable App (Recommended!)

Create a simple shell script that she can double-click:

1. Create a file called `Play.command` in the game folder with this content:
   ```bash
   #!/bin/bash
   cd "$(dirname "$0")"
   python3 valentines_game.py
   ```

2. Make it executable:
   ```bash
   chmod +x Play.command
   ```

3. Now she just double-clicks `Play.command` to play!

---

## 🎨 Customization Guide

### Changing the Celebration Message

Open `valentines_game.py` and find this line near the top:

```python
CELEBRATION_TEXT = "See you on Feb 14 at 11:30\nLove ;)"
```

Change it to whatever you want! Use `\n` for new lines.

### Changing Colors

Find the `COLORS` dictionary and change any colors you like:

```python
COLORS = {
    'background': '#FFE4E8',      # Light pink background
    'cell_selected': '#FF69B4',   # Selected cell color
    # ... etc
}
```

Use hex color codes (Google "hex color picker" to find colors).

### Changing the Timer

```python
GAME_DURATION = 60  # Change to any number of seconds
```

### Changing Points

```python
MAIN_WORD_POINTS = 1_000_000
BONUS_WORD_POINTS = 100
```

---

## 🖼️ Adding Images and GIFs

### Adding Static Images

1. **Install Pillow** (one-time setup):
   ```bash
   pip3 install Pillow
   ```

2. **Create an assets folder:**
   ```bash
   mkdir assets
   ```

3. **Put your images in the assets folder**

4. **Add code to the celebration screen.** Find the `show_celebration` method and add:

```python
# Add this after the hearts labels
try:
    from PIL import Image, ImageTk
    img_path = os.path.join(os.path.dirname(__file__), 'assets', 'your_image.png')
    img = Image.open(img_path)
    img = img.resize((300, 300))  # Adjust size
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
    img_label.image = photo  # Keep reference!
    img_label.pack(pady=20)
except Exception as e:
    print(f"Could not load image: {e}")
```

### Adding Animated GIFs

GIFs are a bit trickier. Here's a helper class you can add to the game:

```python
class AnimatedGIF:
    """Helper class to display animated GIFs in Tkinter."""
    
    def __init__(self, parent, gif_path, bg_color='white'):
        from PIL import Image, ImageTk
        
        self.parent = parent
        self.bg_color = bg_color
        self.frames = []
        self.frame_index = 0
        
        # Load GIF frames
        gif = Image.open(gif_path)
        try:
            while True:
                frame = gif.copy()
                self.frames.append(ImageTk.PhotoImage(frame))
                gif.seek(len(self.frames))
        except EOFError:
            pass
        
        # Create label
        self.label = tk.Label(parent, bg=bg_color)
        self.label.pack(pady=10)
        
        # Get frame duration
        try:
            self.delay = gif.info.get('duration', 100)
        except:
            self.delay = 100
        
        self.animate()
    
    def animate(self):
        self.label.config(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.parent.after(self.delay, self.animate)
```

Then in `show_celebration`:

```python
# Add animated GIF
try:
    gif_path = os.path.join(os.path.dirname(__file__), 'assets', 'cute_gif.gif')
    gif = AnimatedGIF(self.overlay, gif_path, COLORS['celebration_bg'])
except Exception as e:
    print(f"Could not load GIF: {e}")
```

---

## 📁 Project Structure

```
valentines_word_hunt/
├── valentines_game.py    # Main game file
├── Play.command          # Double-click to play (create this)
├── README.md             # This file
├── words.txt             # Optional: custom dictionary
└── assets/               # Your images and GIFs
    ├── photo1.png
    ├── cute_gif.gif
    └── ...
```

---

## 🔧 Troubleshooting

**"Python not found"**
- Mac should have Python 3 pre-installed
- Try `python3` instead of `python`
- Or install from python.org

**Game won't open by double-clicking**
- Right-click the file → Open With → Python Launcher
- Or use the `Play.command` method above

**Images not showing**
- Make sure Pillow is installed: `pip3 install Pillow`
- Check the file path is correct
- Make sure image files are in the `assets` folder

**Dictionary words not working**
- The game uses Mac's built-in dictionary at `/usr/share/dict/words`
- You can also add a custom `words.txt` file with one word per line

---

## 💡 Ideas for Customization

- Add her favorite memes/GIFs to the celebration screen
- Change the colors to her favorites
- Add photos of you two together
- Change the celebration message to include inside jokes
- Add background music (requires pygame library)

---

## Uploading to GitHub

1. Create a new repository on GitHub
2. In Terminal:
   ```bash
   cd /path/to/valentines_word_hunt
   git init
   git add .
   git commit -m "Valentine's Word Hunt game"
   git branch -M main
   git remote add origin https://github.com/yourusername/valentines-word-hunt.git
   git push -u origin main
   ```

Then she can download it from GitHub and run it!

---

Good luck! 💕
