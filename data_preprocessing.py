import cv2


video_path = "C://Users//ghamm//OneDrive//Bureau//UQAC//Hiver//Séminaire//NE1.mp4"
sequences_video_1 = [(0, 10)]  # Séquence de 10 secondes à partir de la minute 1 à la minute 1:10

def extraire_sequences(video, sequences):
    capture = cv2.VideoCapture(video_path) 
    fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codecs pour la vidéo de sortie, ajustez si nécessaire
    
    for index, (debut, fin) in enumerate(sequences):
        capture.set(cv2.CAP_PROP_POS_MSEC, debut*1000)  # Convertir en millisecondes
        success, image = capture.read()
        writer = cv2.VideoWriter("sequence_{}_{}.mp4".format(video, index+1), fourcc, fps, (width, height))
        
        while capture.get(cv2.CAP_PROP_POS_MSEC) <= fin*1000:
            success, image = capture.read()
            if success:
                writer.write(image)
            else:
                break
        
        print("Séquence {} de la vidéo {} extraite avec succès.".format(index+1, video))
        
        writer.release()
    
    capture.release()



extraire_sequences("video_1", sequences_video_1)
