from pytube import YouTube

# Downloads the youtube video specified in the link into the targetDir
def Download(link, targetDir):
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        path = youtubeObject.download(output_path = "data\\video\\full_vids\\" 
                                      + targetDir + "\\")
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    return path
