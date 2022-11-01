# portfolio-back
**To launch server**:
```
docker compose up --build
```
from the root.

**Service setup**
1) Access server shell
```
docker exec -it <server_container_id> bash
```
2) Create new admin user from the shell
```
python manage.py createsuperuser
```
3) Navigate to http://localhost:8000/admin/ and fill the data

**Documentation**
http://localhost:8000/services/swagger/schema