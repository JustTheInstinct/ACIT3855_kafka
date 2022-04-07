FROM ubuntu:18.04 
   
LABEL maintainer="jordangmain@gmail.com" 
 
RUN apt-get update -y && \ 
    apt-get install -y python3 python3-pip && apt-get install python3 

COPY . .

RUN pip3 install -r requirements.txt 

ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]