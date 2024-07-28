from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.views import APIView
from .models import Post,Like,Report,Comment
from .serializers import PostSerializer,PostDetailSerializer,CommentSerializer
from rest_framework.response import Response
from .forms import PostForm,CommentForm
from account.serializers import UserSerializer
from notification.utils import create_notification
from account.models import User, FriendshipRequest

from  .tasks import handle_like


@api_view(['get'])
def post_list(request):
    post=Post.objects.all()
    serilaizer=PostSerializer(post,many=True)
    print(serilaizer.data)
    return JsonResponse(serilaizer.data,safe=False)

@api_view(['get'])
def post_list_friends(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):   
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    # if not request.user in user.friends.all():
    #     posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False
    
    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)


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
        # like = Like.objects.create(created_by=request.user)
        # post = Post.objects.get(pk=pk)
        # post.likes_count = post.likes_count + 1
        # post.likes.add(like)
        # post.save()
        # notification = create_notification(request, 'post_like', post_id=post.id)
        # created_by=request.user
        user_name=request.user.name
        created_by=request.user
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(created_by)
        handle_like.delay(pk, str(created_by),str(user_name), action='like')
        return JsonResponse({'message': 'liked'})
    else:
        # like = post.likes.filter(created_by=request.user)
        # like.delete()
        # post = Post.objects.get(pk=pk)
        # post.likes_count = post.likes_count -1
        # post.save()
        created_by=request.user
        print(created_by)
        user_name=request.user.name
        handle_like.delay(pk, str(created_by),str(user_name), action='dislike')
        return JsonResponse({'message': 'disliked'})




# @api_view(['POST'])
# def post_like(request, pk):
#     post = Post.objects.get(pk=pk)
#     user = request.user

#     if not post.likes.filter(created_by=user).exists():
#         # Like the post
#         like = Like.objects.create(created_by=user)
#         post.likes.add(like)
#         action = 'like'
#     else:
#         # Unlike the post
#         like = post.likes.filter(created_by=user)
#         like.delete()
#         action = 'unlike'
    
#     # Trigger Celery task
#     handle_like.delay(pk, user.id, action)
    
#     # Return response
#     return JsonResponse({'message': 'liked' if action == 'like' else 'disliked'})
    

@api_view(['POST'])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    count=0
    if not post.reports.filter(created_by=request.user):
        report = Report.objects.create(created_by=request.user)
        post = Post.objects.get(pk=pk)
        post.reports_count = post.reports_count + 1
        # count=print(post.reports_count,"report_countiiiii")
        post.reports.add(report)
        post.save()
        notification = create_notification(request, 'post_reported', post_id=post.id)
        return JsonResponse({'message': 'reported'})
    print(count)
    return JsonResponse({'message':'already reported'})

@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})


@api_view(['POST'])
def create_comment(request,pk):
    form=CommentForm(request.data)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.created_by = request.user
        comment.save()
        post=Post.objects.filter(pk=pk)
        post.comments_count = post.comments_count + 1
        post.comments.add(comment)
        post.save()
        serilaizer=PostSerializer(comment)
        return JsonResponse(serilaizer.data,safe=False)
    return JsonResponse({'data':'msg from back'})


@api_view(['GET'])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids))).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })


@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)