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
    query = request.GET.get('q', '')
    video = get_object_or_404(Video, id=video_id)
    
    subtitles = Subtitle.objects.filter(video=video, content__icontains=query)
    
    timestamps = []
    for subtitle in subtitles:
        match = re.search(r'(\d{2}:\d{2}:\d{2},\d{3})', subtitle.content)
        if match:
            timestamps.append(match.group(1))
    
    return JsonResponse({'timestamps': timestamps})

def get_timestamp(subtitle_line):
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    
    match = timestamp_pattern.search(subtitle_line)
    if match:
        start_timestamp = match.group(1)
    
        return start_timestamp.replace(',', '.')
    return '00:00:00'  

