import subprocess 
from PIL import Image

#tester function that creates a video out of all the .jpg files in the current directory
#this function feeds a ffmepg command to the command line tool 
def images_to_video():
	fps= 0.5
	subprocess.call(["ffmpeg","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video4.avi"])

	#for windows users execute this line
	#subprocess.call(["ffmpeg.exe","-y","-r",str(fps),"-i", "%*.jpg","-vcodec","mpeg4", "-qscale","5", "-r", str(fps), "video4.avi"])

images_to_video()