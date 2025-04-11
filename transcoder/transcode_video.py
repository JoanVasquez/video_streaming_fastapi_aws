# 🎥 Video transcoding module for DASH streaming
import subprocess
from typing import List


# 🎬 Configure video stream encoding parameters
def get_video_stream_settings(resolution: str, bitrate: str,
                              stream_index: int) -> List[str]:
    # Returns FFmpeg parameters for a video stream
    return [
        "-map",
        f"[{resolution}]",
        f"-c:v:{stream_index}",  # 🎯 Video codec settings
        "libx264",
        f"-b:v:{stream_index}",  # 📊 Bitrate configuration
        bitrate,
        "-preset",  # ⚡ Encoding speed/quality balance
        "veryfast",
        "-profile:v",  # 📈 H.264 profile settings
        "high",
        "-level:v",
        "4.1",
        "-g",  # 🔄 GOP (Group of Pictures) settings
        "48",
        "-keyint_min",
        "48"
    ]


# 🎞️ Main transcoding function
def transcode_video(input_path: str, output_dir: str) -> None:
    # 📹 Base FFmpeg command with input and scaling filters
    base_cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-filter_complex",
        "[0:v]split=3[v1][v2][v3];"  # 🔀 Split video into 3 streams
        "[v1]scale=640:360:flags=fast_bilinear[360p];"  # 📐 360p scaling
        "[v2]scale=1280:720:flags=fast_bilinear[720p];"  # 📐 720p scaling
        "[v3]scale=1920:1080:flags=fast_bilinear[1080p]"  # 📐 1080p scaling
    ]

    # 🎥 Configure multiple video quality streams
    video_streams = [
        get_video_stream_settings("360p", "1000k", 0),  # 📱 Mobile quality
        get_video_stream_settings("720p", "4000k", 1),  # 💻 Standard quality
        get_video_stream_settings("1080p", "8000k", 2)  # 🖥️ High quality
    ]

    # 🔊 Audio stream configuration
    audio_settings = [
        "-map",
        "0:a",
        "-c:a",
        "aac",
        "-b:a",
        "128k"
    ]

    # 📦 DASH packaging settings
    dash_settings = [
        "-use_timeline",
        "1",
        "-use_template",
        "1",
        "-window_size",
        "5",
        "-adaptation_sets",
        "id=0,streams=v id=1,streams=a",
        "-f",
        "dash",
        f"{output_dir}/manifest.mpd"
    ]

    # 🔧 Combine all settings into final command
    cmd = (base_cmd +
           [param for stream in video_streams for param in stream] +
           audio_settings + dash_settings)

    # ▶️ Execute FFmpeg command
    process = subprocess.run(cmd)

    # ⚠️ Error handling
    if process.returncode != 0:
        print(process.stderr)
        raise RuntimeError("Transcoding failed!")
