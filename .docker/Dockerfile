FROM public.ecr.aws/lambda/python:3.11.2023.11.18.02

RUN yum install -y Cython libxml2-devel libxslt-devel gcc gcc-c++

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy and install requirements
COPY requirements.txt .
RUN  pip3 install -r requirements.txt
