from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date



# Create your views here.
def index(request):
    return render(request,'index.html')

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'admin_home.html')


def user_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['pwd']
        user = authenticate(username= u, password= p)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == "student":
                    login(request,user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    return render(request,'user_login.html', locals())

def recruiter_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Recruiter.objects.get(user=user)
                if user1.type == "recruiter" and user1.status != "pending":
                    login(request, user)
                    error = "no"
                else:
                    error = "not"
            except:
                error = "yes"
        else:
            error = "yes"
    return render(request,'recruiter_login.html', locals())

def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        e = request.POST['email']
        con = request.POST['contact']
        company = request.POST['company']
        gen = request.POST['gender']
        p = request.POST['pwd']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user,mobile=con,image=i,gender=gen,company=company,type="recruiter",status="pending")
            error = "no"
        except:
            error = "yes"

    return render(request,'recruiter_signup.html', locals())


def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']

        con = request.POST['contact']
        gen = request.POST['gender']

        recruiter.user.first_name = f
        recruiter.user.last_name = l
        recruiter.mobile = con
        recruiter.gender = gen

        try:
            recruiter.save()
            recruiter.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            recruiter.image = i
            recruiter.save()
            error = "no"
        except:
            pass
    return render(request,'recruiter_home.html',locals())

def user_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        p = request.POST['pwd']
        try:
            user = User.objects.create_user(first_name=f, last_name = l, username = e, password=p)
            StudentUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="student")
            error = "no"
        except:
            error = "yes"

    return render(request,'user_signup.html', locals())


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        student .user.first_name = f
        student .user.last_name = l
        student .mobile = con
        student .gender = gen

        try:
            student.save()
            student.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            student.image = i
            student.save()
            error = "no"
        except:
            pass
    return render(request,'user_home.html',locals())

def Logout(request):
    logout(request)
    return redirect('index')

def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = StudentUser.objects.all()
    return render(request,'view_users.html',locals())

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student= User.objects.get(id=pid)
    student.delete()
    return redirect('view_users')

def pending_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='pending')
    return render(request,'pending_recruiters.html',locals())

def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    recruiter = Recruiter.objects.get(id=pid)
    if request.method == "POST":
        s = request.POST['status']
        recruiter.status= s
        try:
            recruiter.save()
            error = "no"
        except:
            error="yes"
    d ={'recruiter':recruiter, 'error':error}
    return render(request,'change_status.html',d)

def accepted_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Accept')
    return render(request,'accepted_recruiters.html',locals())

def rejected_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.filter(status='Reject')
    return render(request,'accepted_recruiters.html',locals())

def all_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Recruiter.objects.all()
    return render(request,'all_recruiters.html',locals())

def delete_recruiter(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    student= User.objects.get(id=pid)
    student.delete()
    return redirect('all_recruiters')

def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        o = request.POST['old_password']
        n = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error= "no"
            else:
                error= "not"
        except:
            error= "yes"
    return render(request,'change_passwordadmin.html',locals())

def change_password_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        o = request.POST['old_password']
        n = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error= "no"
            else:
                error= "not"
        except:
            error= "yes"
    return render(request,'change_password_user.html',locals())

def change_password_recruiter(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method == "POST":
        o = request.POST['old_password']
        n = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error= "no"
            else:
                error= "not"
        except:
            error= "yes"
    return render(request,'change_password_recruiter.html',locals())

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    if request.method == 'POST':
        jt = request.POST['jobtitle']
        sd = request.POST['start_date']
        ed = request.POST['end_date']
        sal = request.POST['salary']
        l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        s = request.POST['skills']
        des = request.POST['description']
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter, start_date=sd, end_date=ed, title=jt, salary=sal, image=l, description=des, experience=exp, location=loc, skills=s, creation_date=date.today())
            error = "no"
        except:
            error = "yes"
    return render(request,'add_job.html',locals())

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    return render(request,'job_list.html',locals())

def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        jt = request.POST.get('jobtitle')
        sd = request.POST.get('start_date')
        ed = request.POST.get('end_date')
        sal = request.POST.get('salary')
        l = request.FILES.get('logo')
        exp = request.POST.get('experience')
        loc = request.POST.get('location')
        s = request.POST.get('skills')
        des = request.POST.get('description')

        job.title = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = s
        job.description = des

        try:
            job.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                job.start_date = sd
                job.save()
            except:
                pass
        else:
            pass

        if ed:
            try:
                job.end_date = ed
                job.save()
            except:
                pass
        else:
            pass
    return render(request,'edit_jobdetail.html',locals())


def change_companylogo(request,pid):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    error = ""
    job = Job.objects.get(id=pid)
    if request.method == 'POST':
        cl = request.FILES.get('logo')


        job.image = cl

        try:
            job.save()
            error = "no"
        except:
            error = "yes"

    return render(request,'change_companylogo.html',locals())

def latest_job(request):
    job = Job.objects.all().order_by('-start_date')
    return render(request,'latest_job.html',locals())

def user_latestjob(request):
    job = Job.objects.all().order_by('-start_date')
    user = request.user
    student = StudentUser.objects.get(user=user)
    data = AppliedStudent.objects.filter(student=student)
    li = []
    for i in data:
        li.append(i.job.id)
    return render(request,'user_latestjob.html',locals())

def job_detail(request,pid):
    job = Job.objects.get(id=pid)
    return render(request,'job_detail.html',locals())

def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error = ""
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=pid)

    date1 = date.today()
    if job.end_date < date1:
        error = "close"
    elif job.start_date > date1:
        error = "NotOpenYet"
    else:
        if request.method == 'POST':
            r = request.FILES.get('resume')
            AppliedStudent.objects.create(student=student, job=job, resume=r, applied_date=date.today())
            error = "done"
    return render(request,'applyforjob.html',locals())


def appliedcandidate_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    apply = AppliedStudent.objects.all()
    return render(request,'appliedcandidate_list.html',locals())

def contact(request):
    return render(request,'contact.html')
