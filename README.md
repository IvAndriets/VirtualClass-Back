# VirtualClass-API

## Keycloak settings

### Client setup
1. Add client **virtual-class**
2. Set **Client authentication**, **Authorization** and **Implicit flow**
3. Set **Valid redirect URIs** to your application host e.g. **http://localhost:4200/auth-callback.html**
4. Set **Web origins** to * or your hosts list

### Role model in keycloak 
1. Add different scopes that we like to have **Clients -> Client details -> Authorization -> Scopes**
2. Create application specific roles inside client **Clients -> Client details -> Roles**
3. Add role policies **Clients -> Client details -> Authorization -> Policies**
4. Add scope based Permissions **Clients -> Client details -> Authorization -> Permissions**
5. Assign roles to users
6. Export settings into Django application

## Local Development

### Fill environment variables

DEBUG **0 or 1**

SECRET_KEY **generate application secret**

DJANGO_ALLOWED_HOSTS=* localhost 127.0.0.1 [::1]

DB_HOST **your DB HOST**

DB_NAME **your DB NAME**

DB_USER **your DB USER**

DB_PASS **your DB PASSWORD**

OIDC_RP_CLIENT_SECRET **keycloak -> realm -> keys -> RS256 Key**

OIDC_RP_CLIENT_PUBLIC_KEY **keycloak -> realm -> keys -> RS256 Public Key**

OIDC_RP_CLIENT_ID **Application CLIENT ID**

OIDC_KEYCLOAK_REALM **Realm Name**

KEYCLOAK_SERVER_URL **Keycloak server url e.g. http://127.0.0.1:18080/auth/**



### Run Keycloak and PostgreSQL with docker compose

```shell
docker-compose -f docker-compose.local.yml up -d
```

### Create a virtual environment to isolate package dependencies locally

```shell
python3 -m venv env
source env/bin/activate
```

### Add new project

```shell
django-admin startproject v-class-api .
```

### Add new application

```shell
django-admin startapp your-app-name
```

### Install packages

```shell
pip install -r requirements.local.txt
```

### Create superuser

```shell
./manage.py createsuperuser
```

### Make and apply migrations

```shell
./manage.py makemigrations
./manage.py migrate
```

## Run application locally

```shell
./manage.py runserver
```
