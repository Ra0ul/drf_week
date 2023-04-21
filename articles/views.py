from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework.views import APIView

# Create your views here.


@api_view(['GET', 'POST'])
def articleAPI(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        # article = articles[0]
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # print(request.data['key'])
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def articleDetail(request, article_id):
    if request.method == 'GET':
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(Article, id=article_id)  # 없는 번호 요청이 들어왔을 때
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(
            article, data=request.data)  # 앞에 내용을 새로운 데이터로 수정
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
