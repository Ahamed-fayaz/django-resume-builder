from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML
from .models import *
from django.template.loader import render_to_string
from django.contrib import messages


def home(request):
    return HttpResponse("Resume app is working!")

@login_required
def resume(request):
    if request.method == "POST":
        name = request.POST["fullname"]
        designation = request.POST["designation"]
        email = request.POST["email"]
        phone= request.POST["phone"]
        github= request.POST["github"]
        linkedin= request.POST["linkedin"]
        summary= request.POST["summary"]
        location= request.POST["location"]

        resume = Resume()
        resume.full_name = name
        resume.designation= designation
        resume.email = email
        resume.phone = phone
        resume.github= github
        resume.linkedin= linkedin
        resume.summary= summary
        resume.location= location
        resume.user= request.user

        resume.save()
        messages.success(request, "Resume created successfully")
        return redirect('resume_list')

    return render(request, "resume/resume.html")

@login_required
def resume_list(request):
    resumes=Resume.objects.filter(user=request.user)
    return render(request,
    "resume/resume_list.html",
    context={"resumes":resumes})

@login_required
def resume_detail(request,id):
    resume= Resume.objects.get(id=id, user=request.user)
    educations= Education.objects.filter(resume=resume)
    projects= Project.objects.filter(resume=resume)
    experiences= Experience.objects.filter(resume=resume)
    skills= Skill.objects.filter(resume=resume)
    certifications= Certifications.objects.filter(resume=resume)
    languages= Language.objects.filter(resume=resume)
    categories=["languages","frontend","backend","database","tools","methodologies"]

    skill_categories={}
    for category in categories:
        category_skills= skills.filter(category=category)
        if category_skills:
            skill_categories[category]=(', ').join( [skill.name for skill in category_skills])

    return render(request,"resume/resume_detail.html",{"resume":resume,
    'educations':educations,
    "projects":projects,
    "experience":experiences,
    'skills':skills,
    'certs':certifications,
    "languages":languages,
    'categories':skill_categories})

@login_required
def edit_resume(request,id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method=='POST':
        print(request.POST)
        resume.full_name=request.POST['fullname']
        resume.designation= request.POST['designation']
        resume.email=request.POST['email']
        resume.phone=request.POST['phone']
        resume.github=request.POST['github']
        resume.linkedin=request.POST['linkedin']
        resume.summary=request.POST['summary']
        resume.location= request.POST['location']
        resume.save()
        return redirect('resume_list')
    return render(request,"resume/edit_resume.html",{"details":resume})

@login_required
def delete_resume(request,id):

    if request.method=='POST':
        resume = get_object_or_404(Resume, id=id, user=request.user)
        resume.delete()
        return redirect('resume_list')
    return redirect('resume_list')

# Education
@login_required
def add_ed(request,id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    
    if request.method=='POST':
        degree= request.POST['degree']
        course= request.POST['course']
        completed_year= request.POST['year']
        college=request.POST['college']
        grade= request.POST['grade']
        

        education= Education()
        education.resume=resume
        

        education.degree=degree
        education.course=course
        education.college=college
        education.completed_year=completed_year
        education.grade=grade
        education.save()
        messages.success(request, "Education added successfully")
        return redirect(f'/resumedetail/{resume.id}#education')
    return render(request,"resume/add_education.html",{'resume':resume})

@login_required
def edit_ed(request,id):
    education=get_object_or_404(Education,id=id, resume__user=request.user)
    if request.method=='POST':
        education.degree=request.POST['degree']
        education.course=request.POST['course']
        education.college=request.POST['college']
        education.completed_year=request.POST['year']
        education.grade=request.POST['grade']
        education.save()
        return redirect(f'/resumedetail/{education.resume.id}#education')
    return render(request,'resume/edit_education.html',{'education':education})

@login_required
def del_ed(request,id):
    if request.method=='POST':
        education=get_object_or_404(Education,id=id, resume__user=request.user)
        resume_id = education.resume.id
        education.delete()
        return redirect('resume_detail',id=resume_id)
    return redirect('resume_detail')

# Projects
@login_required
def add_proj(request,id):
    resume=get_object_or_404(Resume,id=id, user=request.user)
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        tools=request.POST['tools']

        project=Project()
        
        project.name= name
        project.description=description
        project.tools=tools
        project.resume=resume
        project.save()
        return redirect(f'/resumedetail/{resume.id}#project')
    return render(request,'resume/add_project.html',{'resume':resume})


@login_required
def edit_proj(request,id):
    project=get_object_or_404(Project,id=id, resume__user=request.user)
    if request.method=='POST':
        project.name=request.POST['name']
        project.description=request.POST['description']
        project.tools=request.POST['tools']
        project.save()
        return redirect(f'/resumedetail/{project.resume.id}#project')

    return render(request,'resume/edit_project.html',{'project':project})


@login_required
def del_proj(request,id):
    project= get_object_or_404(Project,id=id, resume__user=request.user)
    resume_id = project.resume.id
    project.delete()
    return redirect('resume_detail',id=project.resume.id)

# Experience
@login_required
def add_exp(request,id):
    resume=get_object_or_404(Resume,id=id,user=request.user)
    if request.method=='POST':
        company=request.POST['company']
        role=request.POST['role']
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        role_description=request.POST['role_description']

        experience= Experience()
        experience.company=company
        experience.role=role
        experience.start_date= start_date
        experience.end_date= end_date
        experience.role_description= role_description
        experience.resume=resume
        experience.save()
        return redirect(f'/resumedetail/{resume.id}#experience')

    return render(request,'resume/add_experience.html',{'resume':resume})

@login_required
def edit_exp(request,id):

    experience=get_object_or_404(Experience,id=id, resume__user=request.user)
    if request.method=='POST':
        experience.company=request.POST['company']
        experience.role=request.POST['role']
        experience.start_date=request.POST['start_date']
        experience.end_date=request.POST['end_date']
        experience.role_description=request.POST['role_description']
        experience.save()
        return redirect(f'/resumedetail/{experience.resume.id}#experience')

    return render(request,'resume/edit_experience.html',{'experience':experience})

@login_required
def del_exp(request,id):
    experience= get_object_or_404(Experience,id=id,resume__user=request.user)
    resume_id = experience.resume.id
    experience.delete()
    return redirect('resume_detail',id=experience.resume.id)

# Skill
@login_required
def add_skills(request,id):
    resume= get_object_or_404(Resume,id=id,user=request.user)
    if request.method=='POST':
        language=request.POST['languages'].split(',')
        frontend=request.POST['frontend'].split(',')
        backend=request.POST['backend'].split(',')
        database=request.POST['database'].split(',')
        tools=request.POST['tools'].split(',')
        methodologies=request.POST['methodologies'].split(',')
        categories={"languages":language,'frontend':frontend,"backend":backend,"database":database,"tools":tools,"methodologies":methodologies}
        
        for category, skills in categories.items():
            for skill_name in skills:
                skill_name= skill_name.strip()
                if skill_name:
                    skill=Skill()
                    skill.name=skill_name
                    skill.category=category
                    skill.resume=resume
                    skill.save()
        return redirect(f'/resumedetail/{resume.id}#skills')

    return render(request,'resume/add_skill.html',{'resume':resume})

@login_required
def edit_skills(request, id):
    resume= get_object_or_404(Resume,id=id,user=request.user)
    languages=Skill.objects.filter(resume=resume,category="languages")
    frontend=Skill.objects.filter(resume=resume,category="frontend")
    backend=Skill.objects.filter(resume=resume,category="backend")
    database=Skill.objects.filter(resume=resume,category="database")
    tools=Skill.objects.filter(resume=resume,category="tools")
    methodologies=Skill.objects.filter(resume=resume,category="methodologies")
    skill= Skill.objects.filter(resume=resume)
    
    categories={"languages":languages,'frontend':frontend,"backend":backend,"database":database,"tools":tools,"methodologies":methodologies}
    if request.method=='POST':
        skill.delete()
        for category in categories:
            skill_text= request.POST[category]
            for skill_name in skill_text.split(','):
                skill_name=skill_name.strip()
                if skill_name:
                    skill=Skill()
                    skill.name=skill_name
                    skill.category= category
                    skill.resume=resume
                    skill.save()
        return redirect(f'/resumedetail/{resume.id}#skills')
    
    existing={}
    for category, skills in categories.items():
        existing[category]=", ".join([s.name for s in skills])
    return render(request,'resume/edit_skill.html',{'resume':resume,'skill':existing})

@login_required
def delete_skills(request,id):
    skill= get_object_or_404(Skill,id=id, resume__user=request.user)
    resume_id = skill.resume.id
    skill.delete()
    return redirect('resume_detail',id=skill.resume.id)

# Certifications

@login_required
def add_certs(request,id):
    resume=get_object_or_404(Resume,id=id, user=request.user)

    if request.method=='POST':
        names=request.POST['certifications'].split(',')
        for cert_name in names:
            cert_name= cert_name.strip()
            if cert_name:
                Certifications.objects.create(resume=resume,name=cert_name.strip())
        return redirect(f'/resumedetail/{resume.id}#certification')

    return render(request,'resume/add_certifications.html',{'resume':resume})


@login_required
def edit_certs(request,id):
    resume=get_object_or_404(Resume,id=id, user=request.user)
    certs= Certifications.objects.filter(resume=resume)

    if request.method=='POST':
        certs.delete()
        names= request.POST['certifications'].split(',')
        for cert_name in names:
            cert_name= cert_name.strip()
            if cert_name:
                Certifications.objects.create(resume=resume, name=cert_name)
        return redirect(f'/resumedetail/{resume.id}#certification')

    existing=", ".join([c.name for c in certs])
    return render(request,'resume/edit_certifications.html',{'resume':resume,'certs':existing})

@login_required
def delete_certs(request,id):
    cert= get_object_or_404(Certifications, id=id, resume__user=request.user)
    resume_id = cert.resume.id
    cert.delete()
    return redirect('resume_detail',id=cert.resume.id)
    

# Languages
@login_required
def add_lan(request,id):
    resume= get_object_or_404(Resume,id=id,user=request.user)
    if request.method=='POST':
        names=request.POST['languages'].split(',')
        for lang_name in names:
            lang_name=lang_name.strip()
            if lang_name:
                Language.objects.create(resume=resume,name=lang_name)
        return redirect(f'/resumedetail/{resume.id}#language')
    return render(request,'resume/add_language.html',{'resume':resume})

@login_required
def edit_lan(request,id):
    resume= get_object_or_404(Resume,id=id,user=request.user)
    lang=Language.objects.filter(resume=resume)
    if request.method=='POST':
        lang.delete()
        names=request.POST['languages'].split(',')
        for lang_name in names:
            lang_name=lang_name.strip()
            if lang_name:
                Language.objects.create(resume=resume,name=lang_name)
        return redirect(f'/resumedetail/{resume.id}#language')
    existing=", ".join([l.name for l in lang])
    return render(request,'resume/edit_language.html',{'resume':resume,'language':existing})

@login_required
def delete_lan(request,id):
    lang= get_object_or_404(Language,id=id, resume__user=request.user)
    resume_id = lang.resume.id
    lang.delete()
    return redirect('resume_detail',id=lang.resume.id)

# Resume Preview
@login_required
def resume_preview(request,id):
    resume=get_object_or_404(Resume,id=id,user=request.user)
    skill= Skill.objects.filter(resume=resume)
    experiences= Experience.objects.filter(resume=resume)
    projects= Project.objects.filter(resume=resume)
    educations= Education.objects.filter(resume=resume)
    certifications= Certifications.objects.filter(resume=resume)
    languages= Language.objects.filter(resume=resume)
    categories=["languages","frontend","backend","database","tools","methodologies"]

    skill_categories={}
    for category in categories:
        category_skills= skill.filter(category=category)
        if category_skills:
            skill_categories[category]=(', ').join( [skill.name for skill in category_skills])

    for exp in experiences:
        exp.points = [point.strip() for point in exp.role_description.split("\n") if point.strip()]
    for prj in projects:
        prj.points = [point.strip() for point in prj.description.split("\n") if point.strip()]
    return render(request,"resume/resume_preview.html",{'resume':resume,'skill':skill, 'experiences':experiences,'projects':projects,'educations':educations, 'certifications':certifications,'languages':languages,'categories':skill_categories})

#------------Resume_pdf------------#
@login_required
def resume_pdf(request, id):
    resume=get_object_or_404(Resume,id=id, user=request.user)
    skill= Skill.objects.filter(resume=resume)
    experiences= Experience.objects.filter(resume=resume)
    projects= Project.objects.filter(resume=resume)
    educations= Education.objects.filter(resume=resume)
    certifications= Certifications.objects.filter(resume=resume)
    languages= Language.objects.filter(resume=resume)
    categories=["languages","frontend","backend","database","tools","methodologies"]

    skill_categories={}
    for category in categories:
        category_skills= skill.filter(category=category)
        if category_skills:
            skill_categories[category]=(', ').join( [skill.name for skill in category_skills])

    for exp in experiences:
        exp.points = [point.strip() for point in exp.role_description.split("\n") if point.strip()]
    for prj in projects:
        prj.points = [point.strip() for point in prj.description.split("\n") if point.strip()]
    html_string = render_to_string("resume/resume_pdf.html",{'resume':resume,'skill':skill, 'experiences':experiences,'projects':projects,'educations':educations, 'certifications':certifications,'languages':languages,'categories':skill_categories})

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    return response