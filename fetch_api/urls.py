from django.urls import path

from .views import index, results, view_story, story_relationships

app_name = 'fetch_api'
urlpatterns = [
    path('', index, name='index'),
    path('results', results, name='results'),
    path('story/<int:node_id>', view_story, name='view_story'),
    path('fetch/story/<int:node_id>', story_relationships, name='story_relationships')
]
