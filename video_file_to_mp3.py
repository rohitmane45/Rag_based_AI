import os
import subprocess


files = os.listdir("video")
print(files)

for file in files:
    print(file)
    tutorial_num = file.split(" [")[0].split("#")[1]
    print(tutorial_num)
    subprocess.run(["ffmpeg", "-i", f"video/{file}", f"audio/audio_{tutorial_num}.mp3"])

