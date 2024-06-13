# Wellfound Scrapper

```bash
sudo docker stop vacancies_dev_backend
sudo docker stop vacancies_dev_db
sudo /home/docker/bin/sites/vacancies-scrapper-dev.itera-research.com.sh
sudo docker logs vacancies_dev_backend
sudo docker logs vacancies_dev_db

sudo docker exec -it vacancies_dev_backend /bin/bash
```

# Boot up server

```
python manage.py runserver 0.0.0.0:8000
```

# How to start app in background

```
nohup python manage.py runserver 0.0.0.0:8000 &
```

# How to stop app in background
```
ps axf | grep 'python manage.py runserver 0.0.0.0:8000' | grep -v grep | awk '{print "kill " $1}' | bash
```
