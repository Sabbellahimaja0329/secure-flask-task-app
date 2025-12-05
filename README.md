# Secure Flask TaskApp  
A secure, role-based task management web application built with **Flask**, **MySQL**, and modern UI/UX design principles.  
This application was developed for the Secure Web Application Project and demonstrates full-stack development with a focus on **security by design**, **secure coding practices**, and **enterprise-quality structure**.

---

## Features
### Core Functionality
- User registration & login  
- Role-based access control (Admin & User)  
- Create, Read, Update, Delete (CRUD) tasks  
- Status tracking (To-Do, In-Progress, Done)  
- Dashboard with searchable tasks  
- Beautiful, responsive UI with gradient themes  

### Security Features
- Password hashing using **bcrypt**  
- CSRF protection using **Flask-WTF**  
- Server-side input validation  
- Session protection (HTTPOnly cookies, secure config)  
- Protected routes using custom decorators  
- Parameterized SQL queries (prevents SQL injection)  
- Static Application Security Testing (**Bandit**)  
- Safe password storage (bcrypt salted hashes)

---
