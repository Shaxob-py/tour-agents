#
#
# from utils.security import pwd_context
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
# print(get_password_hash("1"))


'satr hkjnlkm,m jami 6000'

# [Unit]
# Description=FastAPI app
# After=network.target
#
# [Service]
# User=www-data
# Group=www-data
# WorkingDirectory=/var/www/online_pdp
# ExecStart=/var/www/tour-agents/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
# Restart=always
#
# [Install]
# WantedBy=multi-user.target





# import ffmpeg

# import os
# import glob


def convert_webm_to_mp4(input_path, output_path):
    try:
        # Ensure the input file exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file {input_path} does not exist")

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Perform the conversion using ffmpeg-python
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, vcodec='libx264', acodec='aac', strict='experimental')
        ffmpeg.run(stream)
        print(f"Successfully converted {input_path} to {output_path}")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def batch_convert_webm_to_mp4(input_dir, output_dir):
    # Find all WebM files in the input directory
    webm_files = glob.glob(os.path.join(input_dir, "*.webm"))

    for webm_file in webm_files:
        # Generate output file path
        base_name = os.path.splitext(os.path.basename(webm_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}.mp4")

        # Convert the file
        convert_webm_to_mp4(webm_file, output_file)


if __name__ == "__main__":
    # Example usage
    input_directory = "servarga deploy qilish.webm"  # Directory containing WebM files
    output_directory = "output_videos"  # Directory to save MP4 files

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Run batch conversion
    batch_convert_webm_to_mp4(input_directory, output_directory)
