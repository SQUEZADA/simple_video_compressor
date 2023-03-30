# you will need to run "brew install ffmpeg" to install ffmpeg and pip install ffmpeg-python
import ffmpeg
import os
import pathlib
import json

def compress_video(input_path, output_path, bitrate):
    """
    Compress a video file using ffmpeg-python while preserving portrait orientation.

    Parameters:
        input_path (str): The path to the input video file.
        output_path (str): The path to save the compressed video file.
        bitrate (str): The target bitrate of the compressed video, in bits per second.

    Returns:
        None
    """
    # Get the video metadata
    # print(pathlib.Path('/', input_path).exists())
    if pathlib.Path('/', input_path).exists() == True:
        if pathlib.Path('/', output_path).exists() == False:
            probe = ffmpeg.probe(input_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            width = int(video_info['width'])
            height = int(video_info['height'])
            # transpose = ""
            # if height > width:
            #     transpose = ffmpeg.transpose(1)
            # else:
            #     transpose = None

            # Compress the video
            input_stream = ffmpeg.input(input_path)
            # if transpose is not None:
            #     input_stream = input_stream.video.filter(transpose)
            output_stream = input_stream #.video #.filter('scale', '-2', f'scale={width}:-2')
            output_stream = output_stream.output(output_path,crf=30, vcodec='libx264', b=bitrate, pix_fmt='yuv420p', profile='baseline', acodec='aac', movflags='faststart')
            ffmpeg.run(output_stream, overwrite_output=True)
            print(f"Compressed video saved at {output_path}")


# Example usage
images = open("directus_files 20230329-155710.json", "r")
for x in images:
  fileInfo = json.loads(x)
  fileTypes = ['video/quicktime','video/x-msvideo','video/3gpp']
  videoCount = 0
  for y in fileInfo:
    if fileTypes.count( y["type"] ):
        input_file = f'/{y["filename_download"]}'
        output_file = f'/compress/video{videoCount}.mp4'
        compress_video(input_file, output_file, bitrate="500k")
        videoCount+=1
images.close()

