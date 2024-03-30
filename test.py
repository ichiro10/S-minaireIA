import cv2

def crop_video(input_video, output_video, x1, y1, x2, y2):
    # Open the video file
    cap = cv2.VideoCapture(input_video)
    
    # Get the frame dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(height,width)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, 30, (x2 - x1, y2 - y1))
    
    # Read until video is completed
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Crop the frame
            cv2.imshow("input", frame) 
            cropped_frame = frame[y1:y2, x1:x2]
            out.write(cropped_frame)
        else:
            break
    
    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage
input_video = "C://Users//aghammaz//Desktop//ProjetSI//SeminaireIA//src//Feature_extraction//sequence_video_16_21.mp4"
output_video = "output_cropped.mp4"
"""""
x1, y1 = 340, 20  # Top-left corner coordinates
x2, y2 = 360, 1024  # Bottom-right corner coordinates
"""
x1, y1 = 550, 65  # Top-left corner coordinates
x2, y2 = 850, 590  # Bottom-right corner coordinates
crop_video(input_video, output_video, x1, y1, x2, y2)