import gradio as gr
from datetime import datetime
import os

#=========================================#
#         Ensure directory exists         #
#=========================================#
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

#=========================================#
#            Processing Video             #
#    for callback wav2lip and whisperx    #
#=========================================#
def process_video(video, audio):
    if video is None and audio is None:
        raise gr.Warning("Please upload a video and audio file")
    elif video is None:
        raise gr.Warning("Please upload a video file")
    elif audio is None:
        raise gr.Warning("Please upload an audio file")

    # Ensure the directory exists
    output_dir = "processed_video"
    ensure_directory_exists(output_dir)
    
    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"processed_video_{timestamp}.mp4"
    output_filepath = os.path.join(output_dir, output_filename)
    
    # later will call code here for the lipsync and dubbing
    # For now, just save the uploaded video as the processed video
    with open(video, 'rb') as infile:
        with open(output_filepath, 'wb') as outfile:
            outfile.write(infile.read())
    
    return output_filepath


#=========================================#
#    Choosing the list of output video    #
#=========================================#
def get_output_video():
    return [
        "video.mp4",
        "video.avi",
        "video.mkv",
        "video.flv",
        "video.wmv",
        "video.mov",
        "video.webm",
    ]

#=========================================#
#            Custom Interface             #
#=========================================#
def get_custom_blocks():
    theme_color = gr.themes.Default(primary_hue="lime")
    title = "Welcome to [idk what name this project called]"
    css = "footer{display:none !important}"
    #""".gradio-container {margin: 0 !important};"""

    return {"theme": theme_color, "title": title, "css": css}


#=========================================#
#          Creating the interface         #
#=========================================#
custom_block = get_custom_blocks()
theme = custom_block["theme"]
title = custom_block["title"]
css = custom_block["css"]

with gr.Blocks(theme = theme, title = title, css = css) as create_interface:

    # Page header
    with gr.Row():
        # The title and description of the web server
        with gr.Column(scale = 12):
            with gr.Column():
                Title = gr.Markdown(
                    f"""
                    <h1 style="color: #7ABF13;">
                    {title}
                    </h1>
                    """
                )
                Desc = gr.Markdown(
                    """
                    This is a web server that will process a video and audio file.
                    The video will be processed using the lipsync and dubbing technique.
                    bla bla bla
                    """
                )

        #space purpose
        with gr.Column(scale = 5):
            pass

        #with gr.Column(scale = 2):
        #    toggle_dark = gr.Button(value="Toggle Dark")

    # Space purpose
    with gr.Row():
        pass

    upload_interface = gr.Interface(
        fn = process_video,
        inputs = [
            gr.Video(label = "Upload Video",
                    sources = "upload"),

            gr.Audio(label = "Upload Dub Audio",
                    sources = "upload"),
        ],
        outputs = gr.Video(label = "Processed Video",
                        show_download_button = True),

        # #All the upload video and audio files will be stored in the "file_tracking" directory
        allow_flagging = "never",
        # flagging_dir = "file_tracking",
    )


#=========================================#
#           Launch the interface          #
#=========================================#
if __name__ == "__main__":
    create_interface.launch()
