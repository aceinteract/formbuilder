from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from .forms import *
from .models import *

from datetime import datetime, timedelta


# Create your views here.
def landing_page(request):
    return HttpResponseRedirect('/dashboard')


@login_required()
def dashboard(request):
    user = request.user
    all_forms = user.form_set.order_by('title')
    recent_forms = user.form_set.order_by('-publishedDate')[:3]

    variables = {
        'recent_forms': recent_forms,
        'all_forms': all_forms,
        'dashboard': True,
    }

    return render(request, "dashboard_index.html", variables)


@login_required()
def reports(request):
    user = request.user
    user_forms = user.form_set.order_by('-publishedDate')

    user_forms_submission_count = []

    for user_form in user_forms:
        user_forms_submission_count.append(user_form.formsubmission_set.count())

    variables = {
        'user_forms_submission_count': user_forms_submission_count,
        'user_forms': user_forms,
        'dashboard': True,
    }

    return render(request, "dashboard_reports.html", variables)


@login_required()
def report(request, form_id):
    form_to_report = get_object_or_404(Form, id=form_id)

    submissions = form_to_report.formsubmission_set.order_by("-publishedDate")

    if form_to_report.user.username != request.user.username:
        raise Http404('Form does not exist')

    variables = {
        'form_to_report': form_to_report,
        'submissions': submissions,
        'dashboard': True,
    }

    return render(request, "dashboard_report.html", variables)


def login_redirection_page(request):
    return HttpResponseRedirect('/login')


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            if user:
                return HttpResponseRedirect('/dashboard')
            else:
                return HttpResponseRedirect('/register')
    else:
        form = RegistrationForm()

    variables = {
        'form': form
    }
    return render(request, "registration/register.html", variables)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def form_new(request):
    if request.method == 'POST':
        form = FormForm(request.POST)
        if form.is_valid():
            form_to_create = form_save(request, form, False)
            return HttpResponseRedirect('/forms/' + str(form_to_create.id))

    else:
        form = FormForm()

    form_title = ""
    form_json = "[]"

    if request.GET['template'] == 'blank':
        form_title = ""
        form_json = "[]"
    if request.GET['template'] == 'contact':
        form_title = "Contact Information"
        form_json = '[{"id": 0,"fieldType": "text","label": "Name","required": true},' \
                    '{"id": 1,"fieldType": "email","label": "Email","required": true},' \
                    '{"id": 2,"fieldType": "date","label": "Date Of Birth","required": true},' \
                    '{"id": 3,"fieldType": "textarea","label": "Address","required": true},' \
                    '{"id": 4,"fieldType": "tel","label": "Phone Number","required": true},' \
                    '{"id": 5,"fieldType": "textarea","label": "Comments","required": false}]'
    if request.GET['template'] == 'feedback':
        form_title = "Customer Feedback"
        form_json = '[{"id": 0,"fieldType": "radio","label": "Feedback Type",' \
                    '"options": ["Comments", "Questions", "Bug Reports", "Feature Request"],"required": true},' \
                    '{"id": 1,"fieldType": "textarea","label": "Feedback","required": true},' \
                    '{"id": 2,"fieldType": "textarea","label": "Suggestions for improvement","required": false},' \
                    '{"id": 3,"fieldType": "text","label": "Name","required": true},' \
                    '{"id": 4,"fieldType": "email","label": "Email","required": true}]'
    if request.GET['template'] == 'event_register':
        form_title = "Event Registration"
        form_json = '[{"id": 0,"fieldType": "text","label": "Name","required": true},' \
                    '{"id": 1,"fieldType": "email","label": "Email","required": true},' \
                    '{"id": 2,"fieldType": "text","label": "Organization","required": false},' \
                    '{"id": 3,"fieldType": "tel","label": "Phone Number","required": true},' \
                    '{"id": 4,"fieldType": "radio","label": "Till when, would you be staying?",' \
                    '"options": ["9 AM","12 PM","3 PM","6 PM","9 PM"],"required": true}]'
    if request.GET['template'] == 'donation_pledge':
        form_title = "Donation PLedge"
        form_json = '[{"id": 0,"fieldType": "text","label": "Name","required": true},' \
                    '{"id": 1,"fieldType": "email","label": "Email","required": true},' \
                    '{"id": 3,"fieldType": "tel","label": "Phone Number","required": true},' \
                    '{"id": 3,"fieldType": "number","label": "Funds to donate (in NGN)",' \
                    '"min": 100,"max": 100000,"required": true}]'

    variables = {
        'form_title': form_title,
        'form_json': form_json,
        'form': form
    }

    return render(request, "form_new.html", variables)


@login_required()
def form_edit(request, form_id):
    form_to_edit = get_object_or_404(Form, id=form_id)

    if form_to_edit.user.username == request.user.username:
        if request.method == 'POST':
            form = FormForm(request.POST)
            if form.is_valid():
                form_save(request, form, form_id)
                return HttpResponseRedirect('/forms/' + form_id)

        else:
            form = FormForm({
                'title': form_to_edit.title,
                'jsonForm': form_to_edit.jsonForm
            })
    else:
        raise Http404('Form does not exist')

    variables = {
        'form': form
    }

    return render(request, "form_edit.html", variables)


def form_save(request, form, form_id):
    if form_id:
        form_to_save = Form.objects.get(id=form_id)
    else:
        form_to_save = Form.objects.create(user=request.user)

    form_to_save.title = form.cleaned_data['title']
    form_to_save.jsonForm = form.cleaned_data['jsonForm']

    form_to_save.save()

    return form_to_save


@login_required()
def form_delete(request, form_id):
    form_to_delete = get_object_or_404(Form, id=form_id)

    if form_to_delete.user.username == request.user.username:
        if request.method == 'GET':
            form_to_delete.delete()
            return HttpResponseRedirect('/dashboard')
    else:
        raise Http404('Form does not exist')


def form_view(request, form_id):
    try:
        form_to_view = Form.objects.get(id=form_id)
    except ObjectDoesNotExist:
        raise Http404('Form does not exist')

    if request.method == 'POST':
        form = FormSubmissionForm(request.POST)
        if form.is_valid():
            form_submission_save(request, form, form_to_view)
            return HttpResponseRedirect('/forms/submit/success')

    else:
        form = FormSubmissionForm()

    variables = {
        'form': form,
        'form_to_view': form_to_view
    }

    return render(request, 'form_view.html', variables)


def form_submission_save(request, form, form_to_submit):
    submission_to_save = FormSubmission.objects.create(form=form_to_submit)
    submission_to_save.jsonSubmission = form.cleaned_data['jsonFormSubmission']

    submission_to_save.save()

    return submission_to_save


@login_required()
def form_submissions(request, form_id):
    form_to_view = get_object_or_404(Form, id=form_id)

    if form_to_view.user.username != request.user.username:
        raise Http404('Form does not exist')

    submissions = form_to_view.formsubmission_set.order_by("-publishedDate")

    variables = {
        'form_to_view': form_to_view,
        'submissions': submissions
    }

    return render(request, 'dashboard_form_submissions.html', variables)


def form_submit_success(request):
    return render(request, "form_submit_success.html")


@login_required()
def account_page(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            user_save(request, form)

    else:
        form = AccountForm({
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'password1': '',
            'password2': ''
        })

    variables = {
        'form': form
    }
    return render(request, "account.html", variables)


def user_save(request, form):
    user = request.user

    user.username = form.cleaned_data['username']
    user.email = form.cleaned_data['email']
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    if form.cleaned_data['password1'] != '':
        user.password = form.cleaned_data['password1'],

    user.save()

    return user


def handle_uploaded_file(file):
    with open('formbuilder/assets/img/forms/' + str(datetime.now().microsecond), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def form_upload_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse(1)
    return HttpResponse(0)
