# Test assignment for a Python developer position at ivelum
## Hacker™ News proxy

Here is the description of the assigment:
https://github.com/ivelum/job/blob/master/challenges/python.md

I've implemented this with Django because ivelum uses Django.
Otherwise, I would probably have done it with Flask.

Run:

```
gunicorn --bind 0.0.0.0:8000 ivelum.wsgi:application
```

Or with Docker:

```
docker build -t hackertm .
docker run -it -p 8000:8000 hackertm
```

Go to:
http://localhost:8000/
