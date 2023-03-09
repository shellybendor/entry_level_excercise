# entry_level_excercise

Create a new service, composed of 3 microservices:

  1. Data Entry - Web API that receives a request with 2 numbers, responds with an id and sends it to RabbitMQ

  2. Data Process - Microservice that reads from RabbitMQ and calculates the sum of two numbers and stores it in Redis based on the id

  3. Results View - Web API that returns the result based on the ID

Stage 2:

  4. Data Process should also write the result of the calculation to kafka

  5. New service that will read the results from kafka and write them in sets of 5 into a file in azure blob storage.
