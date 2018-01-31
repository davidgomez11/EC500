# **Main Function**
  Build a library (preferable in python) that downloads images from a twitter feed, converts them to a video and describes the content of the images in the video.


## **Important Libraries to download:**
  `Tweepy`, `Pillow`, `wget`, `Google Cloud Vision API` and `Google Cloud Storage` libraries, `FFMPEG`

## **Extra Notes**  
You need to make sure that you create a folder in order for `wget` to download the images from the Twitter API into. In my example I used "twitter_images", of which you should store the main script in there, because the `FFMPEG` command runs on images stored in the same directory with it.

Make sure to download `VLC` at http://www.videolan.org/ in order to run the video that is generated from this script.

There are now Google Cloud Storage capabilities, so all you have to do is install those requirements and then run the correct functions and the photos from twitter will be annotated with their labels and be stored in the cloud, until you run another function which would then download those photos from the cloud and create a video of them in your current working directory.


