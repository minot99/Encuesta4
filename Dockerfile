FROM python:latest

RUN mkdir /home/project

RUN pip3 install django
RUN pip3 install django-microsoft-authentication
RUN pip3 install python-dotenv
RUN pip3 install django-tailwind
RUN pip3 install 'django-tailwind[reload]'
RUN pip3 install requests
RUN pip3 install django-crispy-forms 
RUN pip3 install crispy-bootstrap5
RUN pip3 install django-browser-reload
RUN pip install XlsxWriter

WORKDIR /home/project

COPY . .

ENV PORT 8000
EXPOSE 8000
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

