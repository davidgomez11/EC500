# **Main Function**
  For this part of the assignment I had to review a classmate's repo regarding the main API assignment. After that I had to run their functions and upload a video to a local web host.

## **Code Review**
   Here is my review for the this repo `https://github.com/BoxiHuang/EC500`.

   -Can’t even tell which file to use so I think I'm using the first file I found
   
   -Can’t even run it from the beginning
   	
   	-you need to put in a case in which it can take someone else’s directory not your own ('/Users/borishuang/Desktop/EC500/‘)
   	
   	-ran into an issue where when you are trying to add labels to the photo it trys to access a photo that doesn’t 
   	exist. Like say your max photos was 200, the script was trying to access a photo in the range of 210 for some reason. Quick way to fix this is to put a simple try and except block which in the case if you reach a photo that doesn’t exist you can break the for loop as the case of the except block
   	
   	-Put in a case in which you can allow the user to put in how many photos they want to generate rather than generate all the photos from a single Twitter handle. 
   	
   	-Your code definitely doesn’t generate 200 photos (which is a lot already?), it is generating all the photos it can find from a user_timeline. So that means I don’t think you understand what you are doing here, so it makes me wonder if you even wrote this code?
   	
   	-Its not that hard to change the fontsize on an image (regarding your readme)
   	
   	-You downloaded the photos twice? What’s the point of downloading the photos twice just to rename them? You can just run a simple command like image.save(“insert new name”, "JPEG”) after you did image.open, since I see you are using the PIL library. 
   	
   	-Probably should do some error handling, like for that `Twitter` method which searches for media via a user_timeline only works with valid user_names