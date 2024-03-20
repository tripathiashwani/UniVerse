
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from .models import Post,Like
from .serializers import PostSerializer
from rest_framework.response import Response
from .forms import PostForm
from account.serializers import UserSerializer
from account.models import User


@api_view(['get'])
def post_list(request):
    post=Post.objects.all()
    serilaizer=PostSerializer(post,many=True)
    print(serilaizer.data)
    return JsonResponse(serilaizer.data,safe=False)

@api_view(['get'])
def profile_list(request,id):
    user=User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    print(posts)
    post_serialaizer=PostSerializer(posts,many=True)
    user_serializer=UserSerializer(user)
    return JsonResponse({'posts':post_serialaizer.data,'user':user_serializer.data},safe=False)


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


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        # notification = create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'liked'})
    else:
        like = post.likes.filter(created_by=request.user)
        like.delete()
        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count -1
        post.save()
        return JsonResponse({'message': 'disliked'})

# @api_view(['POST'])
# def post_like(request, pk):
#     post = Post.objects.get(pk=pk)

#     try:
#         like = Like.objects.get(created_by=request.user)
#         like.delete()
#         post.likes_count -= 1
#         post.save()
#         return JsonResponse({'message': 'disliked'})
#     except Like.DoesNotExist:
#         like = Like.objects.create(created_by=request.user)
#         post.likes_count += 1
#         post.likes.add(like)
#         post.save()
#         return JsonResponse({'message': 'liked'})