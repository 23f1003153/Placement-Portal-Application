# Placement-Portal-Application

      Placement Portal Application Report 
1. Student Details                                                                                                                                                  
 Name: Chandan kumar                                                                                                                                                
 Roll Number: 23f100315                                                                                                                                             
 Email: 23f1003153@ds.study.iitm.ac.in
                                                                                                                              
     About Me: I am a student at IIT Madras BS Degree program with a deep interest in  web application development and data-driven technologies. I enjoy building meaningful applications that combine learning, analytics, and user experience.  This project demonstrates the design and development of a placement portal using Flask and SQLAlchemy, focusing on role-based access and application management.
   
3. Project Details                                                                                                                                                  
Problem Statement:                                                                                                                                                
    Students often face difficulty tracking placement opportunities and managing applications across multiple companies. Similarly, companies need an organized way     to evaluate candidates and manage recruitment drives. A centralized platform is required to track these activities and provide clear insights into application       status.                                                                                                                                                        
Approach:                                                                                                                                                          
    The application is built using Flask and SQLAlchemy to create a web-based system where students can track available drives and their application status, while      companies can manage recruitment drives and review applicants. The system uses role-based access for students, companies, and administrators to ensure proper       management and workflow of the placement process.
4. AI/LLM Declaration                                                                                                                                               
    I used ChatGPT (GPT-5) to assist in writing SQLAlchemy model definitions, creating API documentation samples, and improving variable naming consistency.
    The extent of AI/LLM usage is around 10–15%, limited to code suggestions and documentation formatting.
     All final implementation logic, debugging, and integration were done manually.
5. Technologies Used                                                                                                                                                
Backend                                                                                                                                                             
    Python : web framework for python used to build the backend of the application.                                                                                 
    Flask : web framework for python used to build the backend of the application.                                                                                
    Flask-SQLAlchemy : Integrates SQLAlchemy into Flask for DB operations.                                                                                        
    Sqlalchemy : ORM(Object Relation Mapping) to interact with the relational databases.                                                                            
Frontend                                                                                                                                                            
    HTML : Structure and markup of web pages.
    Bootstrap (for UI styling) : CSS framework for responsive design.
    Jinja2 Templates : Template engine for python.
Database
    SQLite (for storing user, company, student, drive, and application data): Embedded SQL database used via SQLAlchemy.
6. DB scheme design                                                                                                                                                
User                                                                                                                                                                
    Stores authentication and role information                                                                                                                      
    Columns are id,username,password,email,role,name,is_approved,is_blacklisted                                                                                     
    Central user management table                                                                                                                                   
    Different roles determine system access.                                                                                                                        
Company_Profiles                                                                                                                                                    
    Columns are id, user_id, company_name, description                                                                                                              
    Relationship : one user → one company profile                                                                                                                   
    Stores company specific details.                                                                                                                                
Student_Profiles                                                                                                                                                    
    Columns are id, user_id, department, resume, skills
    Relationship : One user → one student profile
    Stores student academic and skill information                                                                                                                   
Drive                                                                                                                                                               
    Columns are id, company_id, job_title,job_description, salary, location, eligibility, deadline, status, approval_status,created_at                              
    Stores recruitment drive details created by companies.                                                                                                          
Application                                                                                                                                                         
    Columns are id, student_id, drive_id, date_applied, status, remark                                                                                              
    Unique constraint on (student_id, drive_id) ensures a student cannot apply twice for the same drive.                                                            
    Tracks student applications and their recruitment status.                                                                                                                                                                                                                                                                         
API Design                                                                                                                                                         
Authentication                                                                                                                                                     
User Login : /api/login                                                                                                                                            
Student registration : /api/student_signup                                                                                                                         
Company registration : /api/company_signup                                                                                                                        
Logout : /api/logout
                                                                                                                 
Admin API                                                                                                                                                          
For admin dashboard : /api/admin_dashboard                                                                                                                         
For searching student and company : /api/search                                                                                                                    
For giving approval to company drive : /api/approve_drive/<int:drive_id>                                                                                          
For rejecting Company Drive : /api/reject_drive/<int:drive_id>                                                                                                     
For view student application : /api/astudent_application/<int:application_id>                                                                                      
For view drive details : /api/adrive_details/<int:drive_id>                                                                                                        
For approve company registration: /api/approve_company/<int:user_id>                                                                                              
For blacklist user : /api/blacklist_user/<int:user_id>
                                                                                                       
Student API                                                                                                                                                        
For Student Dashboard : /api/student_dashboard                                                                                                                    
For editing their profiles : /api/edit_student_profile                                                                                                             
For view their application : /api/my_applications                                                                                                                  
For view company drive : /api/sdrive_details/<int:drive_id>                                                                                                        
For view company details : /api/company_details/<int:user_id>                                                                                                      
For view drive details : /api/drive_details/<int:drive_id>                                                                                                         
For apply for company drive : /api/apply/<int:drive_id>
                                                                                      
Company API                                                                                                                                                        
For company dashboard : /api/company_dashboard                                                                                                                    
For mark as complete for drive : /api/complete_drive/<int:drive_id>                                                                                                
For update close drive : /api/update_closed_drive/<int:drive_id>                                                                                                  
For update application drive : /api/update_application/<int:drive_id>                                                                                              
For view student application : /api/student_application/<int:application_id>                                                                                      
For update student application status : /api/update_application_status/<int:application_id>/<string:status>                                                        
For create drive : /api/create_drive                                                                                                                               
For remove drive : /api/remove_drive/<int:drive_id>
                                                                                                            
8. Architecture and Features                                                                                                                                       
backend/ :                                                                                                                                                         
models.py : contains database models using sqlalchemy                                                                                                              
database.py : contain import of sqlalchemy                                                                                                                        
controllers.py : contain business logic, manages frontend-related route handling, rendering HTML pages.                                                            
instance/ :                                                                                                                                                       
Holds sqlite database file : placementportal.sqlite3                                                                                                              
static/ :                                                                                                                                                          
Contains css files that styles various HTML pages                                                                                                                  
templates/ :                                                                                                                                                       
All the HTML pages are placed here.                                                                                                                                
venv :                                                                                                                                                             
Contain virtual environment files.                                                                                                                                 
Gitignore :                                                                                                                                                       
Contains files to exclude from git.                                                                                                                                
app.py :                                                                                                                                                           
This is the main entry point of the app. It initializes the Flask app, configures the database, sets up login functionality and registers the routes and APIs.
    
Core Features :                                                                                                                                                   
Authentication :                                                                                                                                                   
There are two types signup : Student and Company                                                                                                                  
Login are same for student, admin, company                                                                                                                        
Admin are pre-exist, admin can only login
                                                                                                                        
Student Dashboard:                                                                                                                                                
View company details, view their ongoing drive and apply for it.                                                                                                  
View their application status                                                                                                                                      
View their History and can edit their profiles
                                                                                                    
Admin Dashboard :                                                                                                                                                  
Approve company, approve or reject their drives and blacklist company and student                                                                                  
Total number of students, total number of company, total number of drive, total number of applications.                                                            
Here also search by username of company and students                                                                                                              
Admin can view company ongoing drive and students applications

Company Dashboard:                                                                                                                                                 
Company can create, update and remove drive.                                                                                                                       
Here all showed all ongoing drive, upcoming drive, closed drive, rejected drive                                                                                    
Company can view number of applicants are applied for drive or they can select, reject or shortlist applications.                                                  
