import cv2
import numpy as np
import time

def number_frames(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video capture is successfully opened
    if not cap.isOpened():
        print("Error: Unable to open video capture.")
        exit()

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Total number of frames:", total_frames)

    # Release the video capture object
    cap.release()
    return total_frames


#distance function
def distance(x,y):
    import math
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2) 

 #function to get coordinates
def get_coords(p1):
    try: return int(p1[0][0][0]), int(p1[0][0][1])
    except: return int(p1[0][0]), int(p1[0][1])

def head_rotation(video_path):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_path2 = video_path.split("//")[-1]

    out = cv2.VideoWriter(video_path2,fourcc, 5.0, (640,480))
        
    #capture source video
    cap = cv2.VideoCapture(video_path)

    # Vérifier si la capture vidéo est ouverte
    if not cap.isOpened():
        print("Erreur: Impossible de lire la vidéo.")
        exit()


    #params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                            qualityLevel = 0.3,
                            minDistance = 7,
                            blockSize = 7 )
    
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    #path to face cascde
    face_cascade = cv2.CascadeClassifier('Feature_extraction//haarcascade_frontalface_alt.xml')


    #define font and text color
    font = cv2.FONT_HERSHEY_SIMPLEX


    #define movement threshodls
    max_head_movement = 20
    movement_threshold = 50
    gesture_threshold = 175

    #find the face in the image
    face_found = False
    frame_num = 0
    while not face_found:
        # Take first frame and find corners in it
        frame_num += 1
        ret, frame = cap.read()
        if not ret:
            print("Erreur: Impossible de lire la première image de la vidéo.")
            exit()

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            face_found = True
        cv2.imshow('image',frame)
        out.write(frame)
        cv2.waitKey(1)
    face_center = x+w/2, y+h/3
    p0 = np.array([[face_center]], np.float32)

    rot= []

    gesture_rot = False
    x_movement = 0
    y_movement = 0
    gesture_show = 60 #number of frames a gesture is shown

    delay = 0.1

    while True:    
        ret,frame = cap.read()
        # Check if there are no more frames to read (video has ended)
        if not ret:
             break
        old_gray = frame_gray.copy()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        cv2.circle(frame, get_coords(p1), 4, (0,0,255), -1)
        cv2.circle(frame, get_coords(p0), 4, (255,0,0))
        
        #get the xy coordinates for points p0 and p1
        a,b = get_coords(p0), get_coords(p1)
        x_movement += abs(a[0]-b[0])
        y_movement += abs(a[1]-b[1])
        
        text = 'x_movement: ' + str(x_movement)
        if not gesture_rot: cv2.putText(frame,text,(50,50), font, 0.8,(0,0,255),2)
        text = 'y_movement: ' + str(y_movement)
        if not gesture_rot: cv2.putText(frame,text,(50,100), font, 0.8,(0,0,255),2)

        # Attendre le délai spécifié 
        time.sleep(delay)
        
        if x_movement <gesture_threshold :
            gesture_rot = 'No'
        if x_movement > gesture_threshold:
            gesture_rot = 'Yes'


        if gesture_rot and gesture_show > 0:
            cv2.putText(frame,'Rotation Gesture Detected: ' + gesture_rot,(50,50), font, 1.2,(0,0,255),3)
            gesture_show -=1
        rot.append(gesture_rot) 
        if gesture_show == 0:
            gesture_rot = False
            x_movement = 0
            y_movement = 0
            gesture_show = 60 #number of frames a gesture is shown
            
        p0 = p1

        cv2.imshow('image',frame)
        out.write(frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    cap.release()

    return rot

def head_nods(video_path):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_path2 = video_path.split("//")[-1]

    out = cv2.VideoWriter(video_path2,fourcc, 5.0, (640,480))
        
    #capture source video
    cap = cv2.VideoCapture(video_path)

    # Vérifier si la capture vidéo est ouverte
    if not cap.isOpened():
        print("Erreur: Impossible de lire la vidéo.")
        exit()


    #params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                            qualityLevel = 0.3,
                            minDistance = 7,
                            blockSize = 7 )
    
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                    maxLevel = 2,
                    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    #path to face cascde
    face_cascade = cv2.CascadeClassifier('Feature_extraction//haarcascade_frontalface_alt.xml')


    #define font and text color
    font = cv2.FONT_HERSHEY_SIMPLEX


    #define movement threshodls
    max_head_movement = 20
    movement_threshold = 50
    gesture_threshold = 175

    #find the face in the image
    face_found = False
    frame_num = 0
    while not face_found:
        # Take first frame and find corners in it
        frame_num += 1
        ret, frame = cap.read()
        if not ret:
            print("Erreur: Impossible de lire la première image de la vidéo.")
            exit()

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(frame_gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            face_found = True
        cv2.imshow('image',frame)
        out.write(frame)
        cv2.waitKey(1)
    face_center = x+w/2, y+h/3
    p0 = np.array([[face_center]], np.float32)

    nods=[]

    gesture_nods = False
    x_movement = 0
    y_movement = 0
    gesture_show = 40 #number of frames a gesture is shown

    delay = 0.1

    while True:    
        ret,frame = cap.read()
        # Check if there are no more frames to read (video has ended)
        if not ret:
             break
        old_gray = frame_gray.copy()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        cv2.circle(frame, get_coords(p1), 4, (0,0,255), -1)
        cv2.circle(frame, get_coords(p0), 4, (255,0,0))
        
        #get the xy coordinates for points p0 and p1
        a,b = get_coords(p0), get_coords(p1)
        x_movement += abs(a[0]-b[0])
        y_movement += abs(a[1]-b[1])
        
        text = 'x_movement: ' + str(x_movement)
        if not gesture_nods: cv2.putText(frame,text,(50,50), font, 0.8,(0,0,255),2)
        text = 'y_movement: ' + str(y_movement)
        if not gesture_nods: cv2.putText(frame,text,(50,100), font, 0.8,(0,0,255),2)

        # Attendre le délai spécifié 
        time.sleep(delay)
        
        if y_movement < gesture_threshold:
             gesture_nods = 'No'
        if y_movement > gesture_threshold:
             gesture_nods = 'Yes'

        if gesture_nods and gesture_show > 0:
            cv2.putText(frame,'Nods Gesture Detected: ' + gesture_nods,(50,50), font, 1.2,(0,0,255),3)
            gesture_show -=1

        nods.append(gesture_nods) 
        if gesture_show == 0:
            gesture_nods = False
            x_movement = 0
            y_movement = 0
            gesture_show = 60 #number of frames a gesture is shown
            
        p0 = p1

        cv2.imshow('image',frame)
        out.write(frame)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    cap.release()

    return nods

def overall_motion(video_path):

    #video_path = "C://Users//aghammaz//Desktop//SIA//SeminaireIA//src//Feature_extraction//ex.mp4"

    cap = cv2.VideoCapture(video_path) 
    ret, first_frame = cap.read() 
    

    # Converts frame to grayscale
    prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY) 

    # Creates an image filled with zero 
    mask = np.zeros_like(first_frame) 

    # Sets image saturation to maximum 
    mask[..., 1] = 255

    # Get original frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('fps:',fps)
    delay = int(1000 / fps)

    # List to store magnitudes
    magnitudes = []

    while(cap.isOpened()): 
        
        ret, frame = cap.read() 
        if not ret:
           break
        
        # Opens a new window and displays the input frame 
        cv2.imshow("input", frame) 
        
        # Converts each frame to grayscale 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # Calculates dense optical flow by Farneback method 
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, 
                                        None, 
                                        0.5, 3, 15, 3, 5, 1.2, 0) 
        
        # Computes the magnitude and angle of the 2D vectors 
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1]) 
        
        # Append magnitude to the list
        magnitudes.append(magnitude)
        
        # Sets image hue according to the optical flow direction 
        mask[..., 0] = angle * 180 / np.pi / 2
        
        # Sets image value according to the optical flow  magnitude (normalized) 
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX) 
        
        # Converts HSV to RGB (BGR) color representation 
        rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR) 
        
        # Opens a new window and displays the output frame 
        cv2.imshow("dense optical flow", rgb) 
        
        # Updates previous frame 
        prev_gray = gray 
        
        # Frames are read by intervals of 1 millisecond
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        

    cap.release() 
    cv2.destroyAllWindows() 

    # Convert magnitudes list to numpy array
    magnitudes = np.array(magnitudes)

    # Calculate average magnitude across all frames
    average_magnitude = np.mean(magnitudes)

    # Calculate temporal dynamics: Standard deviation of magnitudes over time
    temporal_dynamics = np.std(magnitudes)


    return average_magnitude, temporal_dynamics



video_path = "C://Users//ghamm//OneDrive//Bureau//UQAC//Hiver//Séminaire//Feature_extraction//test1.mp4"
number_frames(video_path)

h_rot = head_rotation(video_path)
print(h_rot)

h_nods = head_nods(video_path)
print(h_nods)

average_magnitude, temporal_dynamics = overall_motion(video_path)

print ("average_magnitude:",average_magnitude)
print ("temporal_dynamics:",temporal_dynamics)