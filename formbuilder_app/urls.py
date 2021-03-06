from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^dashboard/reports/$', views.reports, name="dashboard-reports"),
    url(r'^dashboard/reports/(\d+)/$', views.report, name="dashboard-report"),
    url(r'^dashboard/forms/submissions/(\d+)/$', views.form_submissions, name="form-submissions"),

    # Form Management
    url(r'^forms/(\d+)/$', views.form_view, name="form-view"),
    url(r'^forms/new/', views.form_new, name="form-new"),
    url(r'^forms/upload_image/', views.form_upload_image, name="form-upload-image"),
    # url(r'^forms/edit/(\d+)/$', views.form_edit, name="form-edit"),
    url(r'^forms/delete/(\d+)/$', views.form_delete, name="form-delete"),
    url(r'^forms/submit/success', views.form_submit_success, name="form-submit-success"),

    # Account Management
    url(r'^account/$', views.account_page, name="account_page"),

    # Session Management
    url(r'^accounts/login/', views.login_redirection_page, name="login_redirection_page"),
    url(r'^register/$', views.register_page, name="register_page"),
    url(r'^register/success/$', TemplateView.as_view(template_name="registration/register_success.html")),
    url(r'^logout/', views.logout_page, name="logout_page"),
]
