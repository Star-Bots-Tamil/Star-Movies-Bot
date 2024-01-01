from pyrogram import Client, filters
import subprocess

@Client.on_message(filters.command("editmetadata"))
def edit_metadata(client, message):
    if message.reply_to_message and message.reply_to_message.video:
        original_file = message.reply_to_message.video.file_id
        title = message.text.split(" ", 1)[1]  # Extract title from command

        # Download the video
        file_path = client.download_media(original_file)

        # Edit metadata using FFmpeg
        edited_file_path = f"edited_{original_file}.mp4"
        subprocess.run([
            "ffmpeg", "-i", file_path,
            "-metadata", f"title={title}",
            edited_file_path
        ])

        # Send the edited video back to the user
        client.send_video(message.chat.id, edited_file_path, reply_to_message_id=message.reply_to_message.message_id)

        # Clean up files
        subprocess.run(["rm", file_path, edited_file_path])
