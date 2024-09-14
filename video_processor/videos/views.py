from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Subtitle
from django.core.files.storage import FileSystemStorage
import subprocess
from django.http import JsonResponse
from .forms import VideoUploadForm
import re

def video_upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            fs = FileSystemStorage()
            video_path = fs.path(video.file.name)
            output_srt_path = video_path.replace('.webm', '.srt')
            subprocess.run(['ffmpeg', '-i', video_path, '-map', '0:s:0', output_srt_path])
            with open(output_srt_path, 'r', encoding='utf-8') as f:
                subtitles_content = f.read()

            Subtitle.objects.create(video=video, content=subtitles_content)
            return redirect('video_list')
    else:
        form = VideoUploadForm()

    return render(request, 'upload.html', {'form': form})

def video_list(request):
    videos = Video.objects.all().order_by('-upload_time')
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    subtitles = video.subtitles.all()
    return render(request, 'video_detail.html', {'video': video, 'subtitles': subtitles})


def search_subtitle(request, video_id):
    query = request.GET.get('q', '').strip()
    video = get_object_or_404(Video, id=video_id)
    subtitles = Subtitle.objects.filter(video=video)
    timestamps = []
    timestamp_pattern = r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})'
    for subtitle in subtitles:
        blocks = subtitle.content.split('\n\n')  
        for block in blocks:
            lines = block.split('\n')

            if len(lines) >= 3:  
                timestamp_line = lines[1]
                match = re.match(timestamp_pattern, timestamp_line)
                
                if match:
                    start_time = match.group(1) 
                    subtitle_text = ' '.join(lines[2:])  
                    
                    if re.search(re.escape(query), subtitle_text, re.IGNORECASE):
                        timestamps.append(start_time)

    return render(request, 'video_search.html', {'video': video,'timestamps': timestamps,'query': query,})



  