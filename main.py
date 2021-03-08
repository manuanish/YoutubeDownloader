##########################
### YOUTUBE DOWNLOADER ###
##########################


# lib imports
import pytube
from pytube import YouTube
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
import getpass
import os

# script imports
from main_gui import Ui_MainWindow
from PyQt5.QtCore import *
import ui_shadows

# globals
video_title = None
video_author = None
video_views = None
video_link = None
video = None
video_folder_path = None
video_progress = None
video_type = "mp4"
video_valid = False
video_quality_current = "360p"
video_quality_new = None
video_quality_array = []
max_video_quality = 0

# global dictionaries
quality_x_pos = {
    "240p": 5,
    "360p": 49,
    "480p": 93,
    "720p": 137,
    "1080p": 181,
}


#################
### FUNCTIONS ###
#################


def isLinkValid(test_video_link):
    """def isLinkValid(test_video_link): -> test_video_link
    check if youtube video link is valid."""

    try:
        import requests

        data = requests.get("https://www.youtube.com/oembed?format=json&url=" + test_video_link).json()
        if data == "Not Found":
            return False
        else:
            return True
    except:
        return False


def videoQualityToInteger(test_video_quality):
    """def videoQualityToInteger(test_video_quality): -> test_video_quality
    convert str video quality to integer."""

    try:
        test_video_quality = str(test_video_quality[:-1])
        test_video_quality = int(test_video_quality)
        return test_video_quality
    except:
        return 0


def getVideoQualityArray(test_video_link):
    """def getVideoQualityArray(test_video_link): -> test_video_link
    get list of possible video qualities as an array."""

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
    """def getMaxVideoQuality():
    get maximum video quality."""

    global video_quality_array

    array_len = len(video_quality_array)
    global max_video_quality

    for i in range(0, array_len):
        if video_quality_array[i] > max_video_quality:
            max_video_quality = video_quality_array[i]
    return max_video_quality


##################
### SUBPROCESS ###
##################


class GetVideoInfo(QObject):
    """class GetVideoInfo(QObject): -> QObject
    get video info."""

    # signals
    finished = pyqtSignal()

    def run(self):
        # globals
        global video_views
        global video_title
        global video_author
        global video_link
        global video

        video = YouTube(str(video_link))

        # data
        video_views = str(video.views)
        video_title = video.title
        video_author = video.author

        self.finished.emit()


class DownloadVideo(QObject):
    """class DownloadVideo(QObject): -> QObject
    download video."""

    # signals
    progress = pyqtSignal()
    finished = pyqtSignal()
    invalid = pyqtSignal()
    quality = pyqtSignal()

    def run(self):

        # globals
        global video_folder_path
        global video_link
        global video_type
        global video_valid
        global video

        # check quality
        getVideoQualityArray(video_link)
        getMaxVideoQuality()

        # video quality error check
        if max_video_quality < int(videoQualityToInteger(video_quality_current)):
            self.quality.emit()
        else:

            # invalid link check
            try:
                video = YouTube(video_link)
                video_valid = True

                tube = pytube.YouTube(str(video_link), on_progress_callback=self.progress_function)
                self.video_tube = tube.streams.filter(res=video_quality_current).first()
                self.video_tube.download(output_path=video_folder_path,
                                         filename=str(video.title) + " - " + str(video_quality_current))

                self.finished.emit()

            except:
                video_valid = False
                self.invalid.emit()

    def progress_function(self, stream, chunk, bytes_remaining):
        # globals
        global video_progress

        size = self.video_tube.filesize
        video_progress = (round(100 - (bytes_remaining / size) * 100))
        self.progress.emit()


###############
### CLASSES ###
###############


class Window(QMainWindow):
    """class Window(QMainWindow): -> QMainWindow
    main widow for app."""

    def __init__(self):
        """ def __init__(self): -> QMainWindow
        initialize the main gui """

        # init super; main window
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # hide unrequited gui components
        self.ui.disable_background_frame.hide()
        self.ui.downloading_frame.hide()
        self.ui.error_frame.hide()
        self.ui.download_button.setEnabled(False)

        # import shadows
        self.ss = ui_shadows

        # set shadows
        self.ui.main_frame.setGraphicsEffect(self.ss.main_window_shadow)
        self.ui.error_frame.setGraphicsEffect(self.ss.error_frame_shadow)
        self.ui.downloading_frame.setGraphicsEffect(self.ss.download_frame_shadow)

        # connect buttons to functions
        self.ui.save_path_button.clicked.connect(self.openSavePath)
        self.ui.refresh_video_preview_button.clicked.connect(self.getVideoData)
        self.ui.close_button.clicked.connect(self.closeProgram)
        self.ui.download_button.clicked.connect(self.downloadVideoTest)
        self.ui.mp3_radio_button.clicked.connect(self.videoTypeAudio)
        self.ui.mp4_radio_button.clicked.connect(self.videoTypeVideo)
        self.ui.close_error_frame_button.clicked.connect(self.closeErrorFrame)
        self.ui.button_240p.clicked.connect(self.setQuality240p)
        self.ui.button_360p.clicked.connect(self.setQuality360p)
        self.ui.button_480p.clicked.connect(self.setQuality480p)
        self.ui.button_720p.clicked.connect(self.setQuality720p)
        self.ui.button_1080p.clicked.connect(self.setQuality1080p)

        # on line edit edited
        self.ui.video_link_line_edit.textEdited.connect(self.checkFolderValid)

    #####################
    ### WIP FUNCTIONS ###
    #####################

    def videoTypeVideo(self):
        """def videoTypeVideo(self): -> self
        download the video as a mp4 file. WIP"""

        global video_type
        video_type = "mp4"
        print(video_type)

    def videoTypeAudio(self):
        """def videoTypeAudio(self): -> self
        download the video as a mp3 file. WIP"""

        global video_type
        video_type = "mp3"
        print(video_type)

    ####################
    ### UI FUNCTIONS ###
    ####################

    def setQuality240p(self):
        """def setQuality240p(self): -> self
        set video quality to 240p"""

        # globals
        global video_quality_new
        global video_quality_current

        video_quality_new = "240p"

        if video_quality_current != video_quality_new:
            self.animateVideoQuality()

    def setQuality360p(self):
        """def setQuality360p(self): -> self
        set video quality to 360p"""

        # globals
        global video_quality_new
        global video_quality_current

        video_quality_new = "360p"

        if video_quality_current != video_quality_new:
            self.animateVideoQuality()

    def setQuality480p(self):
        """def setQuality480p(self): -> self
        set video quality to 480p"""

        # globals
        global video_quality_new
        global video_quality_current

        video_quality_new = "480p"

        if video_quality_current != video_quality_new:
            self.animateVideoQuality()

    def setQuality720p(self):
        """def setQuality720p(self): -> self
        set video quality to 720p"""

        # globals
        global video_quality_new
        global video_quality_current

        video_quality_new = "720p"

        if video_quality_current != video_quality_new:
            self.animateVideoQuality()

    def setQuality1080p(self):
        """def setQuality1080p(self): -> self
        set video quality to 1080p"""

        # globals
        global video_quality_new
        global video_quality_current

        video_quality_new = "1080p"

        if video_quality_current != video_quality_new:
            self.animateVideoQuality()

    def openSavePath(self):
        """def openSavePath(self): -> self
        open the file dialog frame on button press"""

        # globals
        global video_folder_path
        global video_link

        # file dialog
        dialog = QtWidgets.QFileDialog()
        self.video_save_path = dialog.getExistingDirectory(None, "Select Folder")
        folder_name = os.path.basename(self.video_save_path)  # get folder name
        video_folder_path = self.video_save_path

        # set folder text in gui
        username = getpass.getuser()  # get username
        self.ui.file_location_line_edit.setText("C:\\Users\\" + str(username) + "\\...\\" + folder_name)

        video_link = self.ui.video_link_line_edit.text()

        # set download button enabled
        self.ui.download_button.setEnabled(True)

    def openDownloadedVideo(self):
        """def openDownloadedVideo(self): -> self
        open the file the download video is located
        in after downloading is complete."""

        # globals
        global video_folder_path
        global video_valid

        if video_valid:
            # open folder
            import os
            os.startfile(str(video_folder_path))
            video_valid = False

    def checkFolderValid(self):
        """def checkFolderValid(self): -> self
        check if file path is valid."""

        # globals
        global video_folder_path
        global video_link

        video_link = self.ui.video_link_line_edit.text()

        if video_folder_path is not None:
            self.ui.download_button.setEnabled(True)

    def closeProgram(self):
        """def closeProgram(self): -> self
        exit the program"""

        app.quit()  # quit

    def updateBar(self):
        """def updateBar(self): -> self
        update the video download progress bar."""

        global video_progress
        self.ui.video_downloading_progress_bar.setValue(video_progress)

    def showErrorFrame(self):
        """def showErrorFrame(self): -> self
        show error frame."""

        self.ui.downloading_frame.hide()
        self.ui.disable_background_frame.show()
        self.ui.error_frame.show()

        self.ui.error_message_line_edit.setText("Invalid Link!")

    def showErrorFrameQuality(self):
        """def showErrorFrame(self): -> self
        show error frame."""

        self.ui.downloading_frame.hide()
        self.ui.disable_background_frame.show()
        self.ui.error_frame.show()

        self.ui.error_message_line_edit.setText("Video Quality Too High!")

    def closeErrorFrame(self):
        """def closeErrorFrame(self): -> self
        close the error frame."""

        # globals
        global video_quality_array
        global max_video_quality

        self.ui.disable_background_frame.hide()
        self.ui.error_frame.hide()
        self.thread.quit()

        video_quality_array = []
        max_video_quality = 0

    ##################
    ### ANIMATIONS ###
    ##################

    def animateVideoQuality(self):
        """def animateVideoQuality(self): -> self
        animate the highlight QRect over the current
        selected video quality."""

        # globals
        global video_quality_current
        global video_quality_new
        global quality_x_pos

        # animation
        self.animation = QPropertyAnimation(self.ui.video_quality_highlighter_frame, b"geometry")
        self.animation.setDuration(300)
        self.animation.setStartValue(QRect(int(quality_x_pos[str(video_quality_current)]), 4, 40, 42))
        self.animation.setEndValue(QRect(int(quality_x_pos[str(video_quality_new)]), 4, 40, 42))
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        # finish
        video_quality_current = video_quality_new
        print(video_quality_current)

    ##################
    ### SUBPROCESS ###
    ##################

    def downloadVideoTest(self):
        """def downloadVideoTest(self): -> self
        run the subprocess to download videos."""

        # globals
        global video_link
        global video_title
        global video_views
        global video_author
        global video

        video_link = self.ui.video_link_line_edit.text()

        self.thread = QThread()
        self.worker = DownloadVideo()
        self.worker.moveToThread(self.thread)

        # connect subprocess functions
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateBar)

        # run subprocess
        self.thread.start()
        self.ui.downloading_frame.show()
        self.ui.disable_background_frame.show()

        self.worker.invalid.connect(
            self.showErrorFrame
        )

        self.worker.quality.connect(
            self.showErrorFrameQuality
        )

        self.thread.finished.connect(
            lambda: self.ui.downloading_frame.hide()
        )
        self.thread.finished.connect(
            lambda: self.ui.disable_background_frame.hide()
        )
        self.thread.finished.connect(
            lambda: self.ui.video_downloading_progress_bar.setValue(0)
        )
        self.thread.finished.connect(
            self.openDownloadedVideo
        )

    def getVideoDataSubprocess(self):
        """def getVideoDataSubprocess(self):
        start the subprocess to get youtube video
        data."""

        # globals
        global video_author
        global video_title
        global video_views

        # init subprocess
        self.video_data_thread = QThread()
        self.video_data_worker = GetVideoInfo()
        self.video_data_worker.moveToThread(self.video_data_thread)

        # connect subprocess functions
        self.video_data_thread.started.connect(self.video_data_worker.run)
        # self.video_data_thread.started.connect(self.update)
        self.video_data_worker.finished.connect(self.video_data_thread.quit)
        self.video_data_worker.finished.connect(self.video_data_worker.deleteLater)
        self.video_data_thread.finished.connect(self.video_data_thread.deleteLater)

        # run subprocess
        self.video_data_thread.start()

        self.ui.download_button.setEnabled(False)

        # on subprocess finished connect
        self.video_data_thread.finished.connect(
            lambda: self.ui.download_button.setEnabled(True)
        )
        self.video_data_thread.finished.connect(
            lambda: self.ui.video_author_text.setText(video_author)
        )
        self.video_data_thread.finished.connect(
            lambda: self.ui.video_title_text.setText(video_title)
        )
        self.video_data_thread.finished.connect(
            lambda: self.ui.views_text.setText(str(video_views))
        )

    def getVideoData(self):
        """def getVideoData(self): -> self
       check if link is valid to get video data
       if true start subprocess else display error."""

        # globals
        global video_link
        global video_folder_path

        video_link = self.ui.video_link_line_edit.text()  # get video link

        if not isLinkValid(video_link):

            self.ui.video_title_text.setText("Invalid Youtube Video Link!")
            self.ui.video_author_text.setText("")
            self.ui.views_text.setText("")
        else:
            self.ui.video_title_text.setText("Fetching Data...")
            self.ui.video_author_text.setText("")
            self.ui.views_text.setText("")

            self.getVideoDataSubprocess()


###############
### EXECUTE ###
###############


if __name__ == "__main__":
    """if __name__ == "__main__": -> None
    execute the program."""

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
