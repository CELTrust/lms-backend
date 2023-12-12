# lms-backend
Backend Implementation of LMS for CEL

## Steps to Setup:
- Activate Virtual Python Environment
- Install requirements `pip install requirements.txt`
- Install & PostgreSQL
- Add environment variables - `CEL_DB_HOST`, `CEL_DB_USER`, `CEL_DB_NAME`, `CEL_DB_PASSWORD`
- Run migrations `./manage.py migrate`
- Create Superuser from the terminal if not any `./manage.py createsuperuser`
- Run Server `./manage.py runserver`
- For Admin, go to `/admin`
- For User facing API docs, go to `/api/docs`
