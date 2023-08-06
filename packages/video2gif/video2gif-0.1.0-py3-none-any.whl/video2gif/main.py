import argparse
import ffmpeg
import os
import yt_dlp
import validators

parser = argparse.ArgumentParser()
parser.add_argument("video", help="url or path of the video you'd like to gif-ify")
parser.add_argument("start", type=int, help="start time in seconds")
parser.add_argument("end", type=int, help="end time in seconds")
args = parser.parse_args()

if validators.url(args.video):
    URLS = [args.video]
    if os.path.exists("result/inter.mp4"):
        os.remove("result/inter.mp4")
    ydl_opts = {'final_ext': 'mkv',
                'download_ranges': yt_dlp.utils.download_range_func([], [[args.start, args.end]]),
                'format': 'bv*[ext=mp4]+ba[ext=vorbis]/b[ext=mp4] / bv*+ba/b',
                'outtmpl': {'default': 'result/inter.mp4'}}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)
    stream = ffmpeg.input('result/inter.mp4')
else:
    stream = ffmpeg.input(args.video)
    
        
# stream = ffmpeg.input('result/inter.mkv')
stream = ffmpeg.filter(stream, 'scale', height=300, width=-2).output('result/inter-scale.mp4').run(overwrite_output=True)
stream = ffmpeg.input('result/inter-scale.mp4').filter('palettegen', stats_mode='full').output('result/palettegen_full.png')
stream = ffmpeg.run(stream, overwrite_output=True)
stream = ffmpeg.filter(
         [
            ffmpeg.input('result/inter-scale.mp4'),
            ffmpeg.input('result/palettegen_full.png'),
         
         ],
         filter_name='paletteuse',
         dither='heckbert',
         new='False',
         )
stream = ffmpeg.output(stream, 'result/output.gif',framerate=30)

def run() -> None:
    stream.run(overwrite_output=True)
