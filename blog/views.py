from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, views
# Create your views here.



# Temporary in-memory data (no database)
BLOGS = []
BLOG_ID = 1


class BlogListCreateView(views.APIView):
    def get(self, request):
        """View all blog posts"""
        return Response(BLOGS)

    def post(self, request):
        """Create a new blog post"""
        global BLOG_ID

        title = request.data.get("title")
        content = request.data.get("content")
        author = request.data.get("author")

        if not title or not content or not author:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicate title
        for blog in BLOGS:
            if blog["title"].lower() == title.lower():
                return Response({"error": "A blog post with this title already exists."},
                                status=status.HTTP_400_BAD_REQUEST)

        new_blog = {
            "id": BLOG_ID,
            "title": title,
            "content": content,
            "author": author,
        }
        BLOG_ID += 1
        BLOGS.append(new_blog)
        return Response(new_blog, status=status.HTTP_201_CREATED)


class BlogDetailView(views.APIView):
    def get_blog(self, pk):
        for blog in BLOGS:
            if blog["id"] == pk:
                return blog
        return None

    def get(self, request, pk):
        """View a single blog post"""
        blog = self.get_blog(pk)
        if not blog:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(blog)

    def put(self, request, pk):
        """Update a blog post"""
        blog = self.get_blog(pk)
        if not blog:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        blog["title"] = request.data.get("title", blog["title"])
        blog["content"] = request.data.get("content", blog["content"])
        blog["author"] = request.data.get("author", blog["author"])
        return Response(blog, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Delete a blog post"""
        blog = self.get_blog(pk)
        if not blog:
            return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

        BLOGS.remove(blog)
        return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
