from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from .models import Post, IntruderImage
from rest_framework import viewsets
from .serializers import PostSerializer
from django.http import JsonResponse
from .models import DoorStatus

import datetime

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# views.py

def door_status_update(request):
    if request.method == 'POST':
        door_status = DoorStatus.objects.first()

        if door_status:
            if request.POST.get('action') == 'open':
                door_status.open_door()

                # 문이 열리는 이벤트와 관련된 이미지 및 정보 저장
                intruder_image = IntruderImage.objects.create()

                # 블로그 업데이트 함수 호출
                update_blog_with_intruder_info(intruder_image)

            elif request.POST.get('action') == 'close':
                door_status.close_door()


            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'DoorStatus not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def update_blog_with_intruder_info(intruder_image):
    try:
        blog_post = Post.objects.create(
            title=f"Intruder Detected - {timezone.now()}",
            content=f"An intruder has been detected at {timezone.now()}.",
            published_date=timezone.now(),
        )

        # IntruderImage 모델의 정보를 블로그 글에 추가
        blog_post.intruder_image = intruder_image
        blog_post.save()


    except Exception as e:
        print(f"Error updating blog: {e}")

def update_blog_on_door_close(door_status):
    try:
        if door_status.closed_at and door_status.closed_at.hour == 12 and door_status.closed_at.minute == 0:
            pass

    except Exception as e:
        print(f"Error updating blog on door close: {e}")
def door_status_list(request):
    # 문의 상태 목록을 보여주는 뷰
    door_statuses = DoorStatus.objects.all()
    return render(request, 'blog/door_status_list.html', {'door_statuses': door_statuses})

def door_status_detail(request, pk):
    # 문의 상태 상세 정보를 보여주는 뷰
    door_status = DoorStatus.objects.get(pk=pk)
    return render(request, 'blog/door_status_detail.html', {'door_status': door_status})

def door_statistics(request):
    # 문의 통계를 보여주는 뷰
    door_statuses = DoorStatus.objects.all()
    total_opened = door_statuses.filter(opened=True).count()
    total_closed = door_statuses.filter(opened=False).count()

    # 열린 시간 계산
    total_opened_time = sum((status.opened_at - door_statuses[i - 1].opened_at).seconds
                            for i, status in enumerate(door_statuses[1:], start=1)
                            if status.opened and door_statuses[i - 1].opened)

    return render(request, 'blog/door_statistics.html', {
        'total_opened': total_opened,
        'total_closed': total_closed,
        'total_opened_time': total_opened_time,
    })

class IntruderImage(viewsets.ModelViewSet):
    # queryset을 설정해야 함
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
