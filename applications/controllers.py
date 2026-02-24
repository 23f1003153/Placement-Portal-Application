from flask import Flask, redirect, render_template, request,url_for,session, flash
from flask import current_app as app
from applications.models import *
from datetime import datetime

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        pwd = request.form.get("passwd")
        this_user = User.query.filter_by(username=username).first()

        if this_user and this_user.password == pwd:
            # Check if blacklisted
            if this_user.is_blacklisted:
                return "Your account has been deactivated by the admin.", 403
            
            # Check approval for Company
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
        
        return render_template("incorrect_p.html") # Or flash a message
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        pwd = request.form.get("pwd")
        name = request.form.get("fname")
        role = request.form.get("role")
        user_name  = User.query.filter_by(username=username).first()
        user_email = User.query.filter_by(email=email).first()
        if user_name or user_email:
            return render_template("already.html")
        else:
            new_user = User(username=username, email=email, name=name, password=pwd, role=role,
                is_approved=False, is_blacklisted=False, created_at=datetime.utcnow())

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Wait for admin approval.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/admin_dashboard")
def admin_dashboard():

    pending_companies = User.query.filter_by(
        role="Company",
        is_approved=False
    ).all()

    approved_companies = User.query.filter_by(
        role="Company",
        is_approved=True
    ).all()

    students = User.query.filter_by(role="Student").all()

    return render_template(
        "admin_dashboard.html",
        pending_companies=pending_companies,
        companies=approved_companies,
        students=students,
        
    )

@app.route("/student_dashboard")
def student_dashboard():
    if session.get("role") != "Student":
        return redirect(url_for("login"))

    student = User.query.get(session["user_id"])

    companies = User.query.filter(
        User.role == "Company",
        User.is_approved == True,
        User.is_blacklisted == False
    ).all()

    return render_template(
        "Student_dashboard.html",
        student=student,
        reg_companies=companies
    )
@app.route("/company_dashboard")
def company_dashboard():
    if session.get("role") != "Company":
        return redirect(url_for("login"))

    company = User.query.get(session["user_id"])

    companies = CompanyProfile.query.join(User).filter(
        User.role == "company",
        User.is_approved == True,
        User.is_blacklisted == False
    ).all()

    return render_template(
        "company_dashboard.html",
        company=company,
        reg_companies=companies
    )

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

@app.route("/create_drive", methods=['GET','Post'])
def create_drive():
    if request.method == "POST":
        user_id = session.get("user_id")

        # get company profile linked to logged-in user
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

        # convert deadline safely
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
            status="ongoing"
        )

        db.session.add(new_drive)
        db.session.commit()

        flash("Drive created successfully!", "success")
        return redirect(url_for("company_dashboard"))

    return render_template("create_drive.html")


