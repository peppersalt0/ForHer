# 💕 Word Hunt 💕

A word hunt game with a hidden message. Find the words WILL, YOU, BE, MY, VALENTINE to reveal the question!

## How to Run

1. Install dependencies:
   pip3 install Pillow pygame

2. Double-click Play.command

## Adding Your Own Images & GIFs

1. Put your files in the assets folder

2. Open valentines_game.py and find the show_celebration function

3. Add an image:
   try:
       from PIL import Image, ImageTk
       img = Image.open(os.path.join(assets_path, 'yourfile.png'))
       img.thumbnail((200, 200))
       photo = ImageTk.PhotoImage(img)
       img_label = tk.Label(self.overlay, image=photo, bg=COLORS['celebration_bg'])
       img_label.image = photo
       img_label.place(x=100, y=100)
   except Exception as e:
       print(f"Could not load image: {e}")

4. Add a GIF:
   try:
       gif = AnimatedGIF(
           self.overlay,
           os.path.join(assets_path, 'yourfile.gif'),
           bg_color=COLORS['celebration_bg'],
           max_size=(200, 200)
       )
       gif.label.place(x=100, y=100)
   except Exception as e:
       print(f"Could not load GIF: {e}")

## Customization

Change the celebration message at the top of the file:
CELEBRATION_TEXT = "Your message here"

Change the timer:
GAME_DURATION = 60