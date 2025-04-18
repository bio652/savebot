import asyncio
import tempfile
import os

async def downloadVideo(link:str):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
        temppath = tmpfile.name 
    os.remove(temppath)
    
    process = await asyncio.create_subprocess_exec(
        'yt-dlp', '--max-filesize', '50M', '-o', temppath, link,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        errmessage = stderr.decode()
        print("error with downloading ", errmessage)
        return None
    
    if os.path.exists(temppath):
        print("!success! ", temppath)
        return temppath
    else:
        print("Failed to load file.")
        return None