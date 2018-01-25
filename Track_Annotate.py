'''
The following code is an attempt to assist a user in achieving an autonomous annotation for landmarks/objects of
importance.

This code relies on the OpenCV multi-tracker, whihch is part of the OpenCV_contrib module. Check for more
details here ==>> 1. https://github.com/opencv/opencv_contrib/blob/master/modules/tracking/samples/multitracker.py
                  2. https://docs.opencv.org/3.3.0/d8/d77/classcv_1_1MultiTracker.html
                  3. https://docs.opencv.org/trunk/d5/d07/tutorial_multitracker.html
                  4. https://docs.opencv.org/3.1.0/d5/d07/tutorial_multitracker.html

This code was created to achieve a "csv" file containing annnotation data( Names, Bounding Boxes) of the potential
objects/landmarks. This csv file can easily be used to create a tf.record file( if using Tensorflow)

Input:

Video file or a webcam feed

Output:

CSV File : "Output.csv"

Usage:

1. Run the script, and you will see a window named " Select landmarks or objects". Select a bounding box or ROI 
( Region of Interest) on the window using mouse cursor. Hit Enter or Space Bar to move ahead.
2. It will throw a prompt : "Enter a new landmark name?", this is basically the name of the object of interest. Give a name
and hit Enter.
3. Prompt: " Do you want to annotate more?" 
  -  If "No"  - The tracker gets initated and starts tracking on the video on a new window named " Tracking"
  -  If "Yes" -  You will again get the window named " Select landmarks or objects". Select another bounding box or ROI 
     and hit Enter or Space to move ahead.
  -  It will as you the landmark name, and then if you want to annotate more.
  Note : This script was designed to annotate upto five(5) landmarks on a single frame.
4. Once, you say "No" to the prompt to annotate more, it will start tracking all(or single) landmark(s) and show on the 
" Tracking" window.
5. Press ESC in order to stop the tracking.
6. Sometimes, your potential landmarks will be out of the current frame, but will enter the video at a later point of time, in
this case press Tab to stop the tracking.
7. Prompt: "Do you want to track new landmarks?".
  -  If :Yes"  - You will see the same procedure from steps 1 through 4.
  -  If " No"  - The script will terminate after logging all the details into "Output.csv"
8. In order to exit the script this time, just press "Tab" and say " No" to new landmarks, script will terminate.
9. Whenever, script gets terminated, it will log the details as follows
   
   Reference Header = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]
   


'''


# Importing some important modules

import cv2
import sys
import keyboard
import csv
import numpy as np

# Set key press

k = cv2.waitKey(1) & 0xff

# Initialize few important lists and counters

BBOX = []
lan_name_list = []
frame_count = 1307 # Changed the frame count for new video annotation
new_lan = "yes"
font = cv2.FONT_HERSHEY_SIMPLEX



# Enter your video's path or name if in the same path

video_path = 'New_Data/Video_out_test_1.mp4'
video = cv2.VideoCapture(video_path)
frame_string = raw_input("Enter the frame string")# Ask the frame string according to your need.


# Set up OpenCV mutlti- tracker.

tracker = cv2.MultiTracker_create()
init_once = False


# Read first frame.
ok, frame = video.read()

# Exit if video not opened.
if not ok:
    print("Could not open video")
    sys.exit()
if k==27:
    sys.exit()



frame_count += 1
frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5) # This line will reduce the image to half-size, comment to go original

#  Se up frame format for saving the frame as it is read, make sure that the frame count is set properly

frame_name = "%s%d.jpg"%(frame_string,frame_count)
cv2.imwrite("Frames/%s" %frame_name,frame)



# Select bounding box for the very first frame

bbox1 = cv2.selectROI('Select landmarks or objects', frame)
bbox1 = int(bbox1[0]),int(bbox1[1]), abs(int(bbox1[2])), abs(int(bbox1[3]))
print(bbox1)

# Enter the name for the first landmark

lan_name = raw_input("Enter a new landmark name? ")
if lan_name.upper()!= "none".upper():
    lan_name_list.append(lan_name)


# Save the frame information only when the landmark name is not "None"
# Reference Header = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]

if lan_name.upper()!= "none".upper():
    csv_box = [frame_name,"640","360",lan_name,int(bbox1[0]),int(bbox1[1]), ( int(bbox1[2]) + int(bbox1[0])), (int(bbox1[3])+ int(bbox1[1]))]
    BBOX.append(csv_box)

land_count = 1

# Ask the user if they want to annotate more landmarks in the same frame

Response = raw_input("Do you want to annotate more? ")

# Initialize a dictionary to store new landmarks in a loop

bbox_new = {}

# Allow user to annotate more landmarks

if Response.upper() == "yes".upper():
    Res_again = "yes"
    while(1):
        land_count += 1
        bbox_new[str(land_count)] = cv2.selectROI('tracking', frame)
        bbox_new[str(land_count)] = int(bbox_new[str(land_count)][0]), int(bbox_new[str(land_count)][1]), \
                                    abs(int(bbox_new[str(land_count)][2])), \
                                    abs(int(bbox_new[str(land_count)][3]))

        print(bbox_new[str(land_count)])
        lan_name = raw_input("Enter the new landmark name? ")
        lan_name_list.append(lan_name)
        csv_box = [frame_name, "640", "360", lan_name, int(bbox_new[str(land_count)][0]),
                   int(bbox_new[str(land_count)][1]),
                   ( int(bbox_new[str(land_count)][2]) + int(bbox_new[str(land_count)][0])),
                   (int(bbox_new[str(land_count)][3])+ int(bbox_new[str(land_count)][1]))]
        BBOX.append(csv_box)


        Res_again = raw_input("Do you want to annotate more? ")
        if Res_again.upper() == "no".upper():
            break



land_count = len(lan_name_list)



# Start reading frames from the video until the "Tab" is pressed:
# Note: "Tab" will stop the video and ask the user if they want to annotate new landmarks, in a new frame setup

while (True):
    # Read a new frame
    ok, frame = video.read()

    if not ok:
        break

    if k == 27 or new_lan.upper() == "no".upper():
        break


    # Some setup to save the frame as it is being read

    frame_count += 1
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    frame_name = "%s%d.jpg" % (frame_string, frame_count)
    cv2.imwrite("Frames/%s" % frame_name, frame)



    # Initialize tracker with first frame and bounding box
    if not init_once:
        ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox1)
        for i in range(land_count-1):
            ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox_new[str(land_count)])
            land_count-= 1
        init_once = True



    # Update tracker
    ok, boxes = tracker.update(frame)
    j= 0 # An index defined to keep the annotation right, there is a bug in OpenCV multi-track, it shuffles the
         # the landmarks names

    #count = 0


    # A for loop to annotate landmarks in the frame and keep a track of them

    for i in range(len(lan_name_list)):
        #print(i)
        # p1 = (int(newbox[0]), int(newbox[1]))
        # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        p1 = (int(boxes[i,0]), int(boxes[i,1]))
        p2 = (int(boxes[i,0] + boxes[i,2]), int(boxes[i,1] + boxes[i,3]))
        cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)


# Note: The following if-loops are created to get rid of the bug in the opencv mutli-tracker, it basically takes care
#       of the annotations shuffling.


        if len(lan_name_list)==2:
            if i == 1:
                j = 1
            elif i==0:
                j=0
        if len(lan_name_list)==3:
            if i == 1:
                j = 2
            elif i==2:
                j=1
            elif i==0:
                j=0
        if len(lan_name_list) == 4:
            if i == 1:
                j = 3
            elif i==3:
                  j=1
            elif i==2:
                j=2
            elif i==0:
                j=0
        if len(lan_name_list) == 5:
            if i == 1:
                j = 4
            elif i==4:
                  j=1
            elif i==2:
                j=3
            elif i==3:
                j=2
            elif i==0:
                j=0


        # Show the landmark name over the bounding box
        cv2.putText(frame, lan_name_list[j], (int(boxes[i,0]) + 6, int(boxes[i,1]) - 6), font, 0.5, (0, 0, 255), 1)

        # Save the frame details in the standard format
        csv_box = [frame_name, "640", "360", lan_name_list[j], int(boxes[i,0]), int(boxes[i,1]),
                   (int(boxes[i,2]) + int(boxes[i,0])),
                   (int(boxes[i,3])+ int(boxes[i,1]) )]
        BBOX.append(csv_box)


    # Display result
    cv2.imshow("Tracking", frame)

    # Set key press

    k = cv2.waitKey(1) & 0xff

    # Exit if ESC pressed
    if k == 27:
        break


# The following segment of the code runs only if the user wants to annotate more landmarks in a new frame setup

    if k == 9:

    # Make lan_name_list empty as it causes trouble after "Tab" is pressed

     new_lan = "yes"

     while (new_lan.upper() == "yes".upper()):

         new_lan = raw_input("Do you want to track new landmarks? ")

         if new_lan.upper() == "no".upper():

             break
         if k == 27:
             k=27
             break

         lan_name_list = []
         cv2.destroyWindow("Tracking")


         # Set up tracker.
         tracker = cv2.MultiTracker_create()
         init_once = False

         ok, frame = video.read()
         frame_count += 1
         frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
         frame_name = "%s%d.jpg" % (frame_string, frame_count)
         cv2.imwrite("Frames/%s" % frame_name, frame)


         bbox1 = cv2.selectROI('tracking', frame)
         bbox1 = int(bbox1[0]), int(bbox1[1]), abs(int(bbox1[2])), abs(int(bbox1[3]))
         print(bbox1)
         lan_name = raw_input("Enter a new landmark name? ")
         lan_name_list.append(lan_name)
         if lan_name.upper()!= "none".upper():
            csv_box = [frame_name,"640","360",lan_name,int(bbox1[0]),int(bbox1[1]), (int(bbox1[2]) + int(bbox1[0])),
                       (int(bbox1[3]) + int(bbox1[1]))]
            BBOX.append(csv_box)

         land_count = 1

         Response = raw_input("Do you want to annotate more? ")

         bbox_new = {}

         if Response.upper() == "yes".upper():
            Res_again = "yes"
            while(1):
                land_count += 1
                #print(land_count)
                bbox_new[str(land_count)] = cv2.selectROI('tracking', frame)
                bbox_new[str(land_count)] = int(bbox_new[str(land_count)][0]), int(bbox_new[str(land_count)][1]), abs(
                    bbox_new[str(land_count)][2]), abs(bbox_new[str(land_count)][3])
                print(bbox_new[str(land_count)])
                lan_name = raw_input("Enter the new landmark name? ")
                lan_name_list.append(lan_name)
                csv_box = [frame_name, "640", "360", lan_name, int(bbox_new[str(land_count)][0]),
                           int(bbox_new[str(land_count)][1]),
                           (int(bbox_new[str(land_count)][2]) + int(bbox_new[str(land_count)][0])),
                           (int(bbox_new[str(land_count)][3]) + int(bbox_new[str(land_count)][1]))]
                BBOX.append(csv_box)

                Res_again = raw_input("Do you want to annotate more? ")
                if Res_again.upper() == "no".upper():
                    break



         land_count = len(lan_name_list)
         print(lan_name_list)




        #Header = ["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"]



         while True:
            # Read a new frame
            ok, frame = video.read()

            if not ok:
                break
            frame_count += 1
            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            frame_name = "%s%d.jpg" % (frame_string, frame_count)
            cv2.imwrite("Frames/%s" % frame_name, frame)


          # # Initialize tracker with first frame and bounding box
            if not init_once:
                ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox1)
                for i in range(land_count-1):
                    ok = tracker.add(cv2.TrackerMIL_create(), frame, bbox_new[str(land_count)])
                    land_count-= 1
                init_once = True


            # Update tracker
            ok, boxes = tracker.update(frame)
            #print(ok, boxes)


            j= 0 # An index defined to keep the annotation right

            count = 0
            #for newbox in boxes:
            for i in range(len(lan_name_list)):
                #print(i)
                # p1 = (int(newbox[0]), int(newbox[1]))
                # p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                p1 = (int(boxes[i,0]), int(boxes[i,1]))
                p2 = (int(boxes[i,0] + boxes[i,2]), int(boxes[i,1] + boxes[i,3]))
                cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)

                if len(lan_name_list) == 2:
                    if i == 1:
                        j = 1
                    elif i == 0:
                        j = 0
                if len(lan_name_list)==3:
                    if i == 1:
                        j = 2
                    elif i==2:
                        j=1
                    elif i==0:
                        j=0
                if len(lan_name_list) == 4:
                    if i == 1:
                        j = 3
                    elif i==3:
                          j=1
                    elif i==2:
                        j=2
                    elif i==0:
                        j=0
                if len(lan_name_list) == 5:
                    if i == 1:
                        j = 4
                    elif i==4:
                          j=1
                    elif i==2:
                        j=3
                    elif i==3:
                        j=2
                    elif i==0:
                        j=0
                cv2.putText(frame, lan_name_list[j], (int(boxes[i,0]) + 6, int(boxes[i,1]) - 6), font, 0.5,
                            (0, 0, 255), 1)
                csv_box = [frame_name, "640", "360", lan_name_list[j], int(boxes[i, 0]), int(boxes[i, 1]),
                           (int(boxes[i, 2]) + int(boxes[i, 0])),
                           (int(boxes[i, 3]) + int(boxes[i, 1]))]
                BBOX.append(csv_box)
                #i+=1

            # Display result
            cv2.imshow("Tracking", frame)

            # Exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            #print(bbox1)
            if k == 9:
                break


# The following segment of the code provides a very informative "csv" file, which essentially provides details of all the
# landmarks, along with their bounding box coordinates

with open("output.csv", "w") as f:
    writer = csv.writer(f)
    Header = ["Filename", "Width", "Height", "Class", "xmin", "ymin", "xmax", "ymax"]
    writer.writerow(Header)
    for row in BBOX:
        writer.writerow(row)
print(" Total no. of frames were %d"%frame_count)
