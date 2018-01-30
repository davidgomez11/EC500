from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

#function that adds a label to an image in the current directory
def label_adder(image):
	img = Image.open(str(image))
	draw = ImageDraw.Draw(img)
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("arial.ttf", 20)
	# draw.text((x, y),"Sample Text",(r,g,b))
	draw.text((0, 0),"Sample Text",(255,255,255),font=font)
	img.save(str(image))