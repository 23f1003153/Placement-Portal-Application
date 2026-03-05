
from applications.database import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    role = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    company_profile = db.relationship("CompanyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    student_profile = db.relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    company_name = db.Column(db.String(100))
    # industry = db.Column(db.String(100))
    description = db.Column(db.Text)
    user = db.relationship("User", back_populates="company_profile")
    drives = db.relationship("Drive", back_populates="company", cascade="all, delete-orphan")


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    department = db.Column(db.String(100))
    resume = db.Column(db.String(300))
    skills = db.Column(db.String(200))
    user = db.relationship("User", back_populates="student_profile")

    applications = db.relationship("Application", back_populates="student", cascade="all, delete-orphan")


class Drive(db.Model):
    __tablename__ = "drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey("company_profiles.id"), nullable=False)

    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    salary = db.Column(db.Integer)
    location = db.Column(db.String(100))
    deadline = db.Column(db.DateTime)
    name = db.Column(db.String(120))
    eligibility = db.Column(db.String(120))

   
    status = db.Column(db.String(20), default="ongoing")
    approval_status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("CompanyProfile", back_populates="drives")

    applications = db.relationship("Application", back_populates="drive", cascade="all, delete-orphan")


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("student_profiles.id"), nullable=False)

    drive_id = db.Column(db.Integer, db.ForeignKey("drives.id"), nullable=False)

    date_applied = db.Column(db.DateTime, default=datetime.utcnow)

    # status = db.Column(db.String(50), default="Applied")
    status = db.Column(
    db.Enum("Applied", "Shortlisted", "Rejected", "Selected", name="application_status"),
    default="Applied",
    nullable=False
    )
    remark = db.Column(db.String(200))
    student = db.relationship("StudentProfile", back_populates="applications")
    drive = db.relationship("Drive", back_populates="applications")

    __table_args__ = (db.UniqueConstraint("student_id", "drive_id", name="unique_application"),)