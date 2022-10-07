# gw2-raid-performance-tracker
A raid performance application for gw2 arcdps logs. Created with Python, Django, Celery, RabbitMQ and Postgres

## Development Setup
To create the required directories on your local filesystem (outside of docker) for the  
application run the following script or create them by hand. The given username will be the owner of the dirs.
```
sudo scripts/setup.sh -u <username>
```

After the directories are created create the containers by running the docker-compose file.  
```
docker-compose up -d
```

To start the development server on port 8443 you can run the following command.  
```
python3 EliteInsider/manage.py runserver localhost:8443
```
