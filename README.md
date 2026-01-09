# Distributed Task Queue

It's been a while I wrote something systems oriented, so I have decided to build this project
I will be building a close to production grade distributed Task Queue System
Written purely by hand and research when necessary and minimal AI use just for the fun of it.


## Brief Description

A distributed task queue is a system that that is purely used to distribute, manage and coordinate tasks across different servers or machines.
You can read about distributed task queues here: [Distributed Task Queues by geeksforgeeks](https://www.geeksforgeeks.org/system-design/distributed-task-queue-distributed-systems/)


## Stack

This will be written purely in python using the following core packages:
1. FastAPI for the framework to test
2. Postgres for the database
3. Pydantic Logfire for the logging
4. py-test for testing


## Disclaimer

While I did mention it would be close to production grade, I do understand that some things may be implemented oddly or suboptimally so do well to raise such issues if you do spot them :)
That said, this code should obviously not be used for production unless you test, edit and really play with the code and you're sure you want to use it.
I still recommend official toolings like celery, RabbitMQ and others though.
Have fun :)


## Benchmarks

I will build benchmarks for testing the code in comparison to real production grade code like celery and rabbitMQ
Benchmarks will be carried out in this manner:
- Distributed-py(custom built):
  + For PostgresQL + For Redis
- Celery:
  + For PostgresQL + For Redis
- RabbitMQ:
  + For PostgresQL + For Redis
  
These tests will be carried out over a 100, 1.000 and 10.000 jobs.


# TODOs

- [x] Build script for building the schema and populating the database with said schema
- [ ] Migrate the schema to the database and check if it works
- [ ] Create the worker for the jobs
- [ ] Use postgres SQL language to listen and manage the jobs
- [ ] Create the logger function for the pydantic logger
 
