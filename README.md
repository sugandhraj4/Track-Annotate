# Track-Annotate

## Description 

An OpenCV multi-tracker based video annotation tool for creating a deep-learning training image dataset. This tool takes video or webcam feed as input and allows a user to annotate and track multiple objects in a single frame. This tool is useful for obtaining annotation information along with the object labels in a "CSV" format. The csv file can later be easiy converted to tf.record files for Tensoflow based deep-learning training.

## Table of Contents

- Prerequisites
- Installation
- Usage
- License


## Prerequisites

- OpenCV( with OpenCV contrib module)
- Python 3.3+ or Python 2.7
- macOS or Linux


## Installation

###  - OpenCV

Follow the guidelines in the link below to install OpenCV along with the "contrib" module:

[How to install OpenCV from source on macOS or Ubuntu](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)


## Usage

1. Run the script, and you will see a window named **" Select landmarks or objects"**. Select a bounding box or ROI ( Region of Interest) on this window using a mouse cursor. Hit Enter or Space Bar after making the selection to move ahead.
2. It will throw a prompt : **"Enter a new landmark name?"**, this is basically the name of the object of interest. Give a name and hit Enter.
3. Prompt: **" Do you want to annotate more?"**
  -  If "No"  - The tracker gets initated and starts tracking in another window named **" Tracking"**
  -  If "Yes" -  You will again get a window named " Select landmarks or objects". Select another bounding box or ROI and hit Enter or Space to move ahead and enter the new landark name.
  - You can keep annotating more objects by following the last two steps.
  Note : This script was designed to annotate upto five(5) landmarks on a single frame.
4. Once, you say "No" to the prompt to annotate more, it will start tracking all(or single) landmark(s) and show them on the " Tracking" window.
5. Press ESC in order to stop tracking and get output.
6. Sometimes, your potential landmarks will be out of the current frame, but will enter the video at a later point of time, in this case press **Tab twice** to stop tracking.
7. Prompt: "Do you want to track new landmarks?".
  -  If "Yes"  - You will see the same procedure from steps 1 through 4.
  -  If " No"  - The script will terminate after logging all the details into **"Output.csv"**
8. In order to exit the script this time, just press "Tab twice" and say " No" to new landmarks, script will terminate.
9. Whenever, script gets terminated, it will log the details as follows
   
   Reference Header = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
10. It will happen many a times that you do not have any object/landmark in the frame; this script will still work, if the user gives " None" as the name of the landmark name. In this case, you will see the "Tracking" window with no tracker, and once you see a potential object press **" Tab twice"** and follow the aforementioned procedure. 
   
## License

This project is licensed under the MIT License - see the LICENSE file for details
