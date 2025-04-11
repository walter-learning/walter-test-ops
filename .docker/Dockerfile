FROM public.ecr.aws/lambda/python:3.11.2023.11.18.02

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy and install requirements
COPY requirements.txt .
RUN  pip3 install -r requirements.txt
