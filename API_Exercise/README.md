# **Main Function**
  Build a library (preferable in python) that downloads images from a `Twitter` feed, converts them to a video and describes the content of the images in the video. The main function that this does is download photos from `Twitter`, runs the `Google Cloud Vision API` on the photos and makes labels out of the data from `Google Cloud Vision API` and puts it on the black .jpg file that comes after the original photo. Finally a video is made out of those photos using a `FFMPEG` command.


## **Important Libraries to download:**
  `Tweepy`, `Pillow`, `wget`, `Google Cloud Vision API` and `Google Cloud Storage` libraries, `FFMPEG`

## **Extra Notes**  
If you comment out the last four lines in the `main.py` you can run the functions which doesn't utilize the `Google Cloud Storage` and it'll work accordingly. If you want to run the functions which do utilize `Google Cloud Storage` then comment out the four lines above the last four lines. Still a work in progress regarding some member functions that need to be added or adjusted. 

You also need to manually authenticate your `Google Cloud Vision API` keys by doing something like https://cloud.google.com/vision/docs/auth in which for Mac Users they have to input :
`export GOOGLE_APPLICATION_CREDENTIALS=PATH_TO_KEY_FILE`, Windows Users probably have to do `set` instead of `export`.

Make sure to download `VLC` at http://www.videolan.org/ in order to run the video that is generated from this script IF `QuickTime Player` doesn't work.

There are now Google Cloud Storage capabilities, so all you have to do is install those requirements and then run the correct functions and the photos from `Twitter` will be annotated with their labels and be stored in the cloud, until you run another function which would then download those photos from the cloud and create a video of them in your current working directory.

There are separate member functions which only download images from `Twitter`, makes a video out of files in the current working directory using a `FFMPEG` command, and does the facial and web analysis of a path to a .jpg file through `Google Cloud Vision API`.


