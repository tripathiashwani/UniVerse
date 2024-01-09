
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from .forms import PostForm


@api_view(['get'])
def post_list(request):
    post=Post.objects.all()
    serilaizer=PostSerializer(post,many=True)
    return JsonResponse(serilaizer.data,safe=False)


@api_view(['POST'])
def create_post(request):
    form=PostForm(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serilaizer=PostSerializer(post)
        return JsonResponse(serilaizer.data,safe=False)
    return JsonResponse({'data':'msg from back'})
