from flask import Flask, redirect, render_template, request, url_for, session, flash
from flask import current_app as app
from applications.models import *
from datetime import datetime



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/student_signup", methods=["GET", "POST"])
def student_signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("pwd")
        name = request.form.get("fname")
        department = request.form.get("department")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("User already exists", "error")
            return redirect(url_for("student_signup"))

        new_user = User(
            username=username,
            email=email,
            password=password,
            name=name,
            role="Student",
            is_approved=True,    
            is_blacklisted=False
        )

        db.session.add(new_user)
        db.session.flush()

        profile = StudentProfile(
            user_id=new_user.id,
            department=department
        )
        

        db.session.add(profile)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for("login"))

    return render_template("student_signup.html")


@app.route("/company_signup", methods=["GET", "POST"])
def company_signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("pwd")
        name = request.form.get("company_name")
        description = request.form.get("description")

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("User already exists", "error")
            return redirect(url_for("company_signup"))

        new_company = User(
            username=username,
            email=email,
            password=password,
            name=name,
            role="Company",
            is_approved=False,  
            is_blacklisted=False
        )

        db.session.add(new_company)
        db.session.commit()

        profile = CompanyProfile(
            user_id=new_company.id,
            description=description,
            company_name=name
            
        )

        db.session.add(profile)
        db.session.commit()

        flash("Company registered. Wait for admin approval.", "success")
        return redirect(url_for("login"))

    return render_template("company_signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        pwd = request.form.get("passwd")
        this_user = User.query.filter_by(username=username).first()

        if this_user and this_user.password == pwd:
            if this_user.is_blacklisted:
                return "Your account has been deactivated by the admin.", 403

            if this_user.role == 'Company' and not this_user.is_approved:
                return "Your account is pending admin approval.", 403

            session['user_id'] = this_user.id
            session['role'] = this_user.role

            if this_user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            elif this_user.role == "Company":
                return redirect(url_for("company_dashboard"))
            elif this_user.role == "Student":
                return redirect(url_for("student_dashboard"))
        
        return render_template("incorrect_p.html") 
    return render_template("login.html")



@app.route("/admin_dashboard")
def admin_dashboard():

    pending_companies = User.query.filter_by(
        role="Company",
        is_approved=False
    ).all()

    approved_companies = User.query.filter_by(
        role="Company",
        is_approved=True,
        is_blacklisted=False
    ).all()
    applications = Application.query.join(Drive).filter(
    Drive.company_id == session.get("user_id")
    ).all()
    students = User.query.filter_by(role="Student", is_blacklisted=False).all()
    drives = Drive.query.filter(Drive.status=='ongoing', Drive.approval_status=='Approved').all()
    
    pending_drives = Drive.query.filter_by(approval_status="Pending").all()
    return render_template(
        "admin_dashboard.html",
        pending_companies=pending_companies,
        companies=approved_companies,
        students=students,
        ongoing_drives=drives,
        applications=applications,
        pending_drives=pending_drives
    )


@app.route("/search")
def search():

    query = request.args.get("q")

    users = []

    if query:
        users = User.query.filter(
            User.username.ilike(f"%{query}%")
        ).all()

    return render_template(
        "search.html",
        users=users,
        query=query
    )


@app.route("/approve_drive/<int:drive_id>", methods=["POST"])
def approve_drive(drive_id):
    if session.get("role") != "admin":
        flash("Unauthorized", "error")
        return redirect(url_for("login"))

    drive = Drive.query.get(drive_id)
    if not drive:
        flash("Drive not found", "error")
        return redirect(url_for("admin_dashboard"))

    drive.approval_status = "Approved"
    db.session.commit()

    flash("Drive approved successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/reject_drive/<int:drive_id>", methods=["POST"])
def reject_drive(drive_id):
    if session.get("role") != "admin":
        flash("Unauthorized", "error")
        return redirect(url_for("login"))

    drive = Drive.query.get(drive_id)
    if not drive:
        flash("Drive not found", "error")
        return redirect(url_for("admin_dashboard"))

    drive.approval_status = "Rejected"
    drive.status = "cancelled"

    db.session.commit()

    flash("Drive rejected.", "warning")
    return redirect(url_for("admin_dashboard"))




@app.route("/astudent_application/<int:application_id>")
def astudent_application(application_id):

    if session.get("role") != "admin":
        return redirect(url_for("login"))

    application = Application.query.get_or_404(application_id)

    student_profile = application.student  

    return render_template(
        "astudent_application.html",
        student_profile=student_profile,
        application=application
    )

@app.route("/adrive_details/<int:drive_id>")
def adrive_details(drive_id):

    drive = Drive.query.get_or_404(drive_id)

    return render_template('adrive_details.html', drive=drive)


@app.route("/student_dashboard")
def student_dashboard():

    if session.get("role") != "Student":
        return redirect(url_for("login"))

    student = User.query.get(session["user_id"])

    student_profile = StudentProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    applications = Application.query.filter_by(
        student_id=student_profile.id
    ).all()

    companies = User.query.filter(
        User.role == "Company",
        User.is_approved == True,
        User.is_blacklisted == False
    ).all()

    return render_template(
        "Student_dashboard.html",
        student=student,
        reg_companies=companies,
        applications=applications
    )

@app.route("/edit_student_profile", methods=["GET", "POST"])
def edit_student_profile():

    if session.get("role") != "Student":
        return redirect(url_for("login"))

    user = User.query.get(session.get("user_id"))
    student = user.student_profile

    if request.method == "POST":

  
        user.name = request.form.get("name")
        user.email = request.form.get("email")

        student.department = request.form.get("department")
        student.skills = request.form.get("skills")
        student.resume = request.form.get("resume")

        db.session.commit()

        flash("Profile updated successfully")

        return redirect(url_for("student_dashboard"))

    return render_template(
        "edit_student_profile.html",
        user=user,
        student=student
    )


@app.route("/my_applications")
def my_applications():
    if session.get("role") != "Student":
        return redirect(url_for("login"))

    student_profile = StudentProfile.query.filter_by(
        user_id=session.get("user_id")
    ).first()

    if not student_profile:
        flash("Student profile not found", "error")
        return redirect(url_for("student_dashboard"))

    applications = Application.query.filter_by(
        student_id=student_profile.id
    ).order_by(Application.date_applied.desc()).all()

    return render_template(
        "Student_Application_history.html",
        applications=applications,
        student_profile=student_profile
    )


@app.route("/sdrive_details/<int:drive_id>")
def sdrive_details(drive_id):

    drive = Drive.query.get_or_404(drive_id)

    return render_template('sdrive_details.html', drive=drive)

def auto_close_drive(drive):
    if drive.deadline and drive.deadline < datetime.utcnow():
        if drive.status != "completed":
            drive.status = "completed"
            return True
    return False

@app.route("/company_dashboard")
def company_dashboard():
    if session.get("role") != "Company":
        return redirect(url_for("login"))

    company = User.query.get(session["user_id"])

    if not company or not company.company_profile:
        flash("Company profile not found", "error")
        return redirect(url_for("login"))


    all_drives = company.company_profile.drives

    updated = False
    for drive in all_drives:
        if auto_close_drive(drive):
            updated = True

    if updated:
        db.session.commit()

    upcoming_drive = [d for d in all_drives if d.status == "ongoing" and d.approval_status == "Pending"]
    ongoing_drive = [d for d in all_drives if d.status == "ongoing" and d.approval_status == "Approved"]
    rejected_drive = [d for d in all_drives if d.approval_status == "Rejected"]
    closed_drive = [d for d in all_drives if d.status == "completed"]

    return render_template(
        "company_dashboard.html",
        company=company,
        upcoming_drive=upcoming_drive,
        ongoing_drive=ongoing_drive,
        closed_drive=closed_drive,
        rejected_drive=rejected_drive
    )


@app.route("/complete_drive/<int:drive_id>", methods=["POST"])
def complete_drive(drive_id):

    if session.get("role") != "Company":
        return redirect(url_for("login"))

    drive = Drive.query.get_or_404(drive_id)

    drive.status = "completed"

    db.session.commit()

    flash("Drive marked as completed", "success")

    return redirect(url_for("company_dashboard"))


@app.route("/update_closed_drive/<int:drive_id>", methods=["GET", "POST"])
def update_closed_drive(drive_id):

    if session.get("role") != "Company":
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    drive = Drive.query.get_or_404(drive_id)

    if drive.status != "completed":
        flash("Only closed drives can be updated", "warning")
        return redirect(url_for("company_dashboard"))

    if request.method == "POST":

        drive.name = request.form.get("drivename")
        drive.job_title = request.form.get("jobtitle")
        drive.job_description = request.form.get("description")
        drive.salary = request.form.get("salary")
        drive.eligibility = request.form.get("eligibility")
        drive.location = request.form.get("location")

        deadline_str = request.form.get("deadline")

        if deadline_str:
            drive.deadline = datetime.strptime(deadline_str, "%Y-%m-%d")

        db.session.commit()

        flash("Closed drive updated successfully!", "success")
        return redirect(url_for("company_dashboard"))

    return render_template("update_closed_drive.html", drive=drive)


@app.route("/update_application/<int:drive_id>")
def update_application(drive_id):

    if session.get("role") != "Company":
        return redirect(url_for("login"))

    drive = Drive.query.get_or_404(drive_id)

    applications = Application.query.filter_by(
        drive_id=drive_id
    ).all()

    return render_template(
        "Update_application_drive.html",
        drive=drive,
        applications=applications
    )


@app.route("/student_application/<int:application_id>")
def student_application(application_id):

    if session.get("role") != "Company":
        return redirect(url_for("login"))

    application = Application.query.get_or_404(application_id)

    student_profile = application.student   

    return render_template(
        "student_application.html",
        student_profile=student_profile,
        application=application
    )

@app.route("/update_application_status/<int:application_id>/<string:status>")
def update_application_status(application_id, status):

    if session.get("role") != "Company":
        return redirect(url_for("login"))

    application = Application.query.get_or_404(application_id)

    application.status = status
    db.session.commit()

    return redirect(url_for("student_application", application_id=application_id))


@app.route("/approve_company/<int:user_id>", methods=["POST"])
def approve_company(user_id):

    if session.get("role") != "admin":
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    company = User.query.get(user_id)

    if not company or company.role != "Company":
        flash("Invalid company", "error")
        return redirect(url_for("admin_dashboard"))

    company.is_approved = True
    db.session.commit()

    flash(f"{company.name} approved successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/blacklist_user/<int:user_id>")
def blacklist_user(user_id):
    if session.get("role") != "admin":
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    user = User.query.get(user_id)
    user.is_blacklisted = True
    db.session.commit()

    flash("User blacklisted", "warning")
    return redirect(url_for("admin_dashboard"))

@app.route("/create_drive", methods=['GET','POST'])
def create_drive():
    if request.method == "POST":
        user_id = session.get("user_id")

        company_profile = CompanyProfile.query.filter_by(user_id=user_id).first()

        if not company_profile:
            flash("Company profile not found", "error")
            return redirect(url_for("company_dashboard"))
        
        name = request.form.get("drivename")
        job_title = request.form.get("jobtitle")
        description = request.form.get("description")
        salary = request.form.get("salary")
        eligibility = request.form.get("eligibility")
        deadline_str = request.form.get("deadline")
        location = request.form.get("location")

        deadline = None
        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d")

        new_drive = Drive(
            company_id=company_profile.id,
            name=name,
            job_title=job_title,
            job_description=description,
            salary=salary,
            eligibility=eligibility,
            deadline=deadline,
            location=location,
            status="ongoing",
            approval_status="Pending"
        )


        db.session.add(new_drive)
        db.session.commit()

        flash("Drive created successfully!", "success")
        return redirect(url_for("company_dashboard"))

    return render_template("create_drive.html")

@app.route("/remove_drive/<int:drive_id>", methods=["POST"])
def remove_drive(drive_id):

    if session.get("role") != "Company":
        flash("Unauthorized access", "error")
        return redirect(url_for("login"))

    drive = Drive.query.get_or_404(drive_id)

    company_profile = CompanyProfile.query.filter_by(
        user_id=session.get("user_id")
    ).first()

    if drive.company_id != company_profile.id:
        flash("You cannot delete this drive", "error")
        return redirect(url_for("company_dashboard"))

    db.session.delete(drive)
    db.session.commit()

    flash("Drive removed successfully", "success")
    return redirect(url_for("company_dashboard"))


@app.route("/company_details/<int:user_id>")
def company_details(user_id):

    details = CompanyProfile.query.filter_by(user_id=user_id).first()

    if not details:
        return "Company not found", 404

    drives = Drive.query.filter(
        Drive.company_id == details.id,
        Drive.approval_status == "Approved",
        Drive.status == "ongoing"
    ).all()

    return render_template(
        'company_details.html',
        details=details,
        drives=drives
    )


@app.route("/drive_details/<int:drive_id>")
def drive_details(drive_id):

    drive = Drive.query.get_or_404(drive_id)

    return render_template('drive_details.html', drive=drive)


@app.route("/apply/<int:drive_id>", methods=["POST"])
def apply_to_drive(drive_id):
    if session.get("role") != "Student":
        flash("Only students can apply", "error")
        return redirect(url_for("login"))

    student_profile = StudentProfile.query.filter_by(
        user_id=session.get("user_id")
    ).first()

    if not student_profile:
        flash("Student profile not found", "error")
        return redirect(url_for("student_dashboard"))

    drive = Drive.query.get(drive_id)
    if not drive:
        flash("Drive not found", "error")
        return redirect(url_for("student_dashboard"))
    

    existing = Application.query.filter_by(
        student_id=student_profile.id,
        drive_id=drive_id
    ).first()

    if existing:
        flash("You already applied to this drive", "warning")
        return redirect(url_for("student_dashboard"))

    new_application = Application(
        student_id=student_profile.id,
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(new_application)
    db.session.commit()

    flash("Application submitted successfully!", "success")
    return redirect(url_for("student_dashboard"))


@app.route("/logout")
def logout():
    session.clear()   
    return redirect(url_for("login"))