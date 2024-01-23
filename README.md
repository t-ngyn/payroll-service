# payroll-service

## Setup

`pip install -r requirements.txt`

## Run

`uvicorn app:application`

## Endpoints

### POST

`/api/reports/upload`

```
curl  -X POST \
  'http://127.0.0.1:8000/api/reports/upload' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)' \
  --form 'file=@/Users/tnguyen/payroll-service/time-report-42.csv'
```

### GET

`/api/reports?type=payroll`

```
curl  -X GET \
  'http://127.0.0.1:8000/api/reports?type=payroll' \
  --header 'Accept: */*' \
  --header 'User-Agent: Thunder Client (https://www.thunderclient.com)'
```

## Answer to Questions

### How did you test that your implementation was correct?

Using Postman/Thunder Client to query the API and test for various cases to make sure it met all requirements.

### If this application was destined for a production environment, what would you add or change?

- Set limit on the number of rows (For example, can only process maximum 10,000 rows)
- Avoid reading all rows into memory (consider cases with very large files)
- Add Logging and Observability (Like Datadog)
- Add Tests
- Integrate tools to check test coverage
- Add configuration file to integrate into CI/CD pipeline
- Add API Authentication
- Use HTTPS for API
- Add API Rate Limiting
- Multi-Region Deployment
- Encrypt Database
- Add API Gateway/Reverse Proxy/Load Balancer
- Add API Versioning
- Configure Dependabot to manage dependencies
- Add Pre Commit Linting (black, flake8, bandit, etc.)
- Implement Caching
- Add a database constraint for hours worked (greater than zero and less than or equal to 24)
- Dockerize the application and run using gunicorn
- Increase number of workers on gunicorn
- Build a docker image for the application and store in a registry
- Add App Versioning (Semantic Versions)
- Run the report generation asynchronously (in a job like Celery)
- Use server sent events to stream the report back to the client

### What compromises did you have to make as a result of the time constraints of this challenge?

- Use a managed database service (Render)