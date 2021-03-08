from pytube import YouTube
import pytube
import requests


def test(test_link):
    try:
        data = requests.get("https://www.youtube.com/oembed?format=json&url=" + test_link).json()
        if data == "Not Found":
            print("invalid")
        else:
            print("valid")
    except:
        print("invalid")





# video = pytube.YouTube("https://www.youtube.com/watch?v=DkU9WFj8sYo")
# video.streams.filter(res="240p").first().download()

test("https://www.youtube.com/watch?v=ygAvPgyPdlg")

# video = youtube.streams.first()
# video.download("C:\\Users\\manuanish\\PycharmProjects\\YoutubeToMp3-Mp4\\videopath")
