import os
import subprocess

from filmography.models import Filmography


def convert_video(source, resolution):
    
    """
        Extract the filename and extension of the source file
        Create the name of the new file with the desired resolution 
        Define the available resolution options
    """
    print("tasks - 1. Statement") 
    source_name, source_extension = os.path.splitext(source)
    print("tasks - 2. Statement") 
    new_name = f'{source_name}_{resolution}.mp4'
    print("tasks - 3. Statement") 
    
    resolution_options = {
        '480p': 'hd480',
        '720p': 'hd720',
        '1080p': 'hd1080',
    }
    
    """
        Check if the specified resolution is valid
        If not, print an error message and exit the function
        Build the ffmpeg command for the conversion
    """

    if resolution not in resolution_options:
 
        print(f'Ungültige Auflösung: {resolution}')
        return
    
    cmd = (
        f'ffmpeg -i "{source}" -s {resolution_options[resolution]} '
        f'-c:v libx264 -crf 23 -c:a aac -strict -2 "{new_name}"'
    )
    
    print("tasks - 5. Statement") 
    """
        Start the conversion process using subprocess.Popen
        Wait for the conversion process to complete
        Extract the filename of the source file
    """
    conversion_process = subprocess.Popen(cmd, shell=True)
    print("tasks - 6. Statement") 
    conversion_process.wait()
    print("tasks - 7. Statement") 

    file_name = os.path.basename(source)
    print("tasks - 8. Statement") 
    
    """
        Try to find the Video object in the database
        Create the new relative path for the converted file
        Set the new path as an attribute for the specific resolution in the Video object
        Save the updated Video object in the database
        If the Video object is not found, print an error message
    """     
    
    try:
        print("tasks - 9. Statement") 
        video = Filmography.objects.get(video_file__icontains=file_name)
        print("tasks - 10. Statement") 
        new_relative_path = f'videos/{os.path.basename(new_name)}'
        print("tasks - 11. Statement") 
        setattr(video, f'video_file_{resolution}', new_relative_path)
        print("tasks - 12. Statement") 
        video.save()
        print("tasks - 13. Statement") 
    except Filmography.DoesNotExist:
        print(f'Video mit Dateinamen {file_name} nicht gefunden.')