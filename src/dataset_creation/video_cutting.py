import cv2

def extraire_sequences(originPath, targetPath, video, sequences):
    capture = cv2.VideoCapture(originPath)
    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codecs pour la vidéo de sortie, ajustez si nécessaire
    
    for index, (debut, fin) in enumerate(sequences):
        capture.set(cv2.CAP_PROP_POS_MSEC, debut*1000)  # Convertir en millisecondes
        success, image = capture.read()
        writer = cv2.VideoWriter(targetPath + "sequence_{}_{}.mp4".format(video, index+1), 
                                 fourcc, fps, (width, height))
        
        while capture.get(cv2.CAP_PROP_POS_MSEC) <= fin*1000:
            success, image = capture.read()
            if success:
                writer.write(image)
            else:
                break
        
        print("Séquence {} de la vidéo {} extraite avec succès.".format(index+1, video))
        
        writer.release()
    
    capture.release()
