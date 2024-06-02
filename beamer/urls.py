from django.urls import path

from beamer import views


urlpatterns = [
    path('compo-slideshow/<int:pk>', views.CompoSlideshow.as_view(), name='control-beamer'),
    path('preview/<int:pk>', views.PreviewEntry.as_view(), name='preview-entry'),
]
