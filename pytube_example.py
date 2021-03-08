import pytube
from pytube import YouTube

video_quality_array = []
video = None


def videoQualityToInteger(test_video_quality):
    try:
        test_video_quality = str(test_video_quality[:-1])
        test_video_quality = int(test_video_quality)
        return test_video_quality
    except:
        return 0


def getVideoQualityArray(test_video_link):
    global video_quality_array
    global video

    video = YouTube(str(test_video_link))
    for a in video.streams:
        # print(str(a.resolution))
        res_int = videoQualityToInteger(a.resolution)
        # print(res_int)
        video_quality_array.append(res_int)

    video_quality_array = set(video_quality_array)
    video_quality_array = list(video_quality_array)


def getMaxVideoQuality():
    global video_quality_array

    array_len = len(video_quality_array)
    largest_element = 0

    for i in range(0, array_len):
        if video_quality_array[i] > largest_element:
            largest_element = video_quality_array[i]
    return largest_element


video_link = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
video_quality_current = "360p"
video_folder_path = "C:\\Users\\manuanish\\PycharmProjects\\YoutubeToMp3-Mp4\\videopath"

getVideoQualityArray(video_link)
print(getMaxVideoQuality())

# video = YouTube(video_link)
# for i in video.streams:
#     print(str(i.resolution))
# video_valid = True
# tube = pytube.YouTube(str(video_link))
# video_tube = tube.streams.filter(res=video_quality_current).first()
# video_tube.download(output_path=video_folder_path,
#                     filename=str(video.title) + " - " + str(video_quality_current))
# print("done!")
