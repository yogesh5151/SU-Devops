# Enterprise Student Record and Academic Management Platform

Student parallel implementation for the DevOps mini-project. The project demonstrates a Flask academic application, automated testing, Jenkins CI, Docker containerization, and Kubernetes/Minikube deployment.

## Technology Stack

- Python / Flask
- Pytest / pytest-cov
- Flake8
- Git / GitHub
- Jenkins
- Docker
- Kubernetes / Minikube

## Project Structure

```text
student-academic-platform/
├── app/
│   ├── routes/api.py
│   ├── services/student_service.py
│   ├── services/marks_mgmt.py
│   ├── models/
│   └── __init__.py
├── database/db.py
├── tests/
│   ├── test_student_service.py
│   ├── test_marks_mgmt.py
│   └── test_api_endpoints.py
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
├── .dockerignore
├── .gitignore
└── run.py
```

## Business Rules

- Students can enroll in courses.
- Duplicate enrollment is rejected.
- Maximum semester credits: 18.
- A grade can only be recorded after enrollment.
- GPA is calculated using course credits and grade points.

## Local Execution

```bash
python -m venv venv
# Windows PowerShell: .\venv\Scripts\Activate.ps1
# Linux/WSL: source venv/bin/activate
pip install -r requirements.txt
pytest -v --cov=app tests/
python run.py
```

Health endpoint:

```text
http://localhost:5000/api/health
```

## Docker

```bash
docker build -t student-academic-platform:v1.0.0 .
docker images
docker run -d -p 5000:5000 --name student-academic-container student-academic-platform:v1.0.0
docker ps
```

Health check:

```text
http://localhost:5000/api/health
```

Cleanup:

```bash
docker stop student-academic-container
docker rm student-academic-container
```

## Minikube / Kubernetes

Start Minikube with the Docker driver. Build the image in the Minikube Docker environment, then apply the manifests.

```bash
minikube start --driver=docker
eval $(minikube docker-env)
docker build -t student-academic-platform:v1.0.0 .
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -l app=student-academic-platform -o wide
kubectl get svc student-academic-service
```

The Service uses NodePort `30090` and the Deployment runs 3 replicas.

Self-healing demonstration:

```bash
kubectl delete pod $(kubectl get pods -l app=student-academic-platform -o jsonpath='{.items[0].metadata.name}')
kubectl get pods -w
```

Access the application:

```bash
minikube service student-academic-service --url
```

## Required Branch Progression

Use the assignment's topic progression:

```text
feature/foundation
feature/core-app
feature/automated-tests
feature/jenkins-ci
feature/dockerization
feature/kubernetes-orchestration
main
```

## API Summary

- `GET /api/health`
- `GET /api/students`
- `POST /api/students`
- `GET /api/students/<student_id>`
- `GET /api/courses`
- `POST /api/enrollments`
- `GET /api/enrollments`
- `POST /api/grades`
- `GET /api/students/<student_id>/grades`
- `GET /api/students/<student_id>/gpa`
