import os, shutil
import cv2
import pandas as pd

PROCESSED_DIR_PATH = "processed"
CROP_INFO = {"0": {
        "x":311,
        "y":0,
        "width":160,
        "height":359
    }}
def detectPoses(imagePath: str, newVideoPath: str):
    imgName = os.path.splitext(os.path.basename(imagePath))[0]
    
    os.system("FaceLandmarkImg.exe -gaze -tracked -f " + imagePath \
              + " -out_dir " + PROCESSED_DIR_PATH)
    path_to_image = os.path.join(PROCESSED_DIR_PATH, imgName)
    returnValue = None
    csvPath = os.path.join(PROCESSED_DIR_PATH, imgName + ".csv")
    if os.path.exists(csvPath):
        if os.path.exists(path_to_image + ".jpg"):
            os.rename(path_to_image + ".jpg", os.path.join(newVideoPath,
                                                            imgName + ".jpg"))
        returnValue = csvPath
    os.remove(imagePath)
    
    return returnValue


def show_local_mp4_video(file_name, width=640, height=480):
  import io
  import base64
  from IPython.display import HTML
  video_encoded = base64.b64encode(io.open(file_name, 'rb').read())
  return HTML(data='''<video width="{0}" height="{1}" alt="test" controls>
                        <source src="data:video/mp4;base64,{2}" type="video/mp4" />
                      </video>'''.format(width, height, video_encoded.decode('ascii')))

def sequenceProcessingInit(dirPath):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    if os.path.exists(PROCESSED_DIR_PATH):
        shutil.rmtree(PROCESSED_DIR_PATH)
    os.mkdir(PROCESSED_DIR_PATH)

def cropImage(vid_number, img):
    y = CROP_INFO[vid_number]["y"]
    x = CROP_INFO[vid_number]["x"]
    height = CROP_INFO[vid_number]["height"]
    width = CROP_INFO[vid_number]["width"]
    img = img[y:y+height, x:x+width]
    return img

if __name__ == '__main__':
    projectPath = os.path.abspath(".")
    csvPath = os.path.join(projectPath,"src/Training/extracted_features1.csv")
    videoFolderPath = os.path.join(projectPath,"data/video/sequences")
    openFaceFolderPath = os.path.join(projectPath,"data/OpenFace")
    features = pd.read_csv(csvPath)
    
    os.chdir("lib/OpenFace")
    for index, row in features.iterrows():
        vidName = row["File"]
        target = "neurotic" if row["Target"] == "NE" else "confident"
        videoPath = os.path.join(videoFolderPath, target, vidName)
        sequence_name = vidName.split(".")[0]
        vid_number = sequence_name.split("_")[2]
        outputDirPath = os.path.join(openFaceFolderPath, target, sequence_name)

        if not os.path.exists(outputDirPath):
            print(f"Current video: {vidName}")
            sequenceProcessingInit(outputDirPath)
            capture = cv2.VideoCapture(videoPath)
            frame_index = 0
            listDF = []
            while capture.isOpened():
                # Capture frame-by-frame from the camera
                ret, img = capture.read()
                if ret is True:
                    if vid_number in CROP_INFO:
                        img = cropImage(vid_number, img)
                    imagePath = os.path.join("processed", str(frame_index) + ".png")
                    cv2.imwrite(imagePath, img)
                    csvFile = detectPoses(imagePath, outputDirPath + "/")
                    if csvFile != None:
                        listDF.append(pd.read_csv(csvFile))
                        os.remove(csvFile)
                    frame_index += 1
                # Break the loop
                else:
                    break
                if frame_index % 25 == 0:
                    if len(listDF) > 0:
                        mainDF : pd.DataFrame = pd.concat(listDF)
                        mainDF.to_csv(outputDirPath + ".csv", index=False)

            # Release everything:
            capture.release()
            #out.release()
            cv2.destroyAllWindows()
            if len(listDF) > 0:
                mainDF : pd.DataFrame = pd.concat(listDF)
                mainDF.to_csv(outputDirPath + ".csv", index=False)
