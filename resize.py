from PIL import Image

image = Image.open('managepage.png')
new_image = image.resize((250, 250))
new_image.save('managepage.png')
