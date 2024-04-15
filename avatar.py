
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

# Path to your avatar image and audio file
avatar_image_path = 'path/to/avatar_image.png'
audio_file_path = 'path/to/speech_audio.mp3'

# Load your avatar image
avatar_clip = ImageClip(avatar_image_path)

# Load the audio file
audio_clip = AudioFileClip(audio_file_path)

# Set the duration of the image clip to the duration of the audio clip
avatar_clip = avatar_clip.set_duration(audio_clip.duration)

# Set the audio of the image clip to be the audio clip
avatar_clip = avatar_clip.set_audio(audio_clip)

# Create the final video
final_video = CompositeVideoClip([avatar_clip])

# Write the result to a file
final_video_path = 'path/to/final_avatar_video.mp4'
final_video.write_videofile(final_video_path, fps=24)