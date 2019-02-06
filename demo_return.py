import os
def return_video_path():
    s = os.listdir('./videos')
    return_s = []
    for i in s:
        if i[-4:] != '.mp4':
            pass
        else:
            return_s.append(i)
    return return_s


print (return_video_path())