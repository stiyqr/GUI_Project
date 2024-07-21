import gradio as gr
from datetime import datetime
import os

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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{timestamp}.mp4"
    output_filepath = os.path.join(output_dir, output_filename)
    
    # later will call code here for the lipsync and dubbing
    # For now, just save the uploaded video as the processed video
    with open(video, 'rb') as infile:
        with open(output_filepath, 'wb') as outfile:
            outfile.write(infile.read())
    
    return output_filepath


#=========================================#
#    Showing all the processed video      #
#=========================================#
def get_all_processed_videos():
        output_dir = "processed_video"
        processed_videos = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith('.mp4')]

        # Ensure the list has exactly 10 elements
        update_show = processed_videos + [None] * (10 - len(processed_videos))
        
        # Update the btn_list with video paths
        updates = []
        for video_path in update_show:
            if video_path is not None:
                filename = os.path.basename(video_path)
                updates.append(gr.update(value=video_path, label=filename, visible=True))
            else:
                updates.append(gr.update(visible=False))
        
        return updates

video_list = []


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
                        show_download_button = True, autoplay = False),

        # #All the upload video and audio files will be stored in the "file_tracking" directory
        allow_flagging = "never",
        # flagging_dir = "file_tracking",
    )

    with gr.Row():
        for i in range(7):
            btn = gr.Video(visible=False)
            video_list.append(btn)

    run_button = gr.Button("Show All Output")
    run_button.click(get_all_processed_videos, None, video_list)


#=========================================#
#           Launch the interface          #
#=========================================#
if __name__ == "__main__":
    create_interface.launch()
