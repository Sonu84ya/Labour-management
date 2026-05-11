from django.urls import path
from . import views

urlpatterns = [
    path('',                                    views.job_list_view,           name='job_list'),
    path('post/',                               views.post_job_view,           name='post_job'),
    path('my-jobs/',                            views.my_jobs_view,            name='my_jobs'),
    path('review/',                             views.submit_review_view,      name='submit_review'),
    path('<int:job_id>/',                       views.job_detail_view,         name='job_detail'),
    path('<int:job_id>/edit/',                  views.edit_job_view,           name='edit_job'),
    path('<int:job_id>/apply/',                 views.apply_job_view,          name='apply_job'),
    path('application/<int:app_id>/<str:action>/', views.update_application_view, name='update_application'),
]
