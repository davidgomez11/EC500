import subprocess 
from PIL import Image

#tester function that creates a video out of all the .jpg files in the current directory
def images_to_video():
	fps= 1
	subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video4.avi"])
