# Summative_Flask-SQLA-Workout-App-Backend
To view add and delete from the database you can run app.py or run the commands bellow.
## GET ALL
``> curl http://localhost:5555/exercises `` <br>
``> curl http://localhost:5555/workouts``
## GET BY ID
``> curl http://localhost:5555/exercises/[ID] `` <br>
``> curl http://localhost:5555/workouts/[ID]``
## POST
### adding a exercise example
``> curl -X POST http://localhost:5555/exercises -H "Content-Type: application/json" -d "{\"name\": \"Pull-ups\", \"category\": \"Upper Body\", \"equipment_needed\": false}"``
### adding a workout example
``> curl -X POST http://localhost:5555/workouts -H "Content-Type: application/json" -d "{\"date\": \"2024-01-18\", \"duration_minutes\": 45, \"notes\": \"Evening session\"}"``
### adding exercise to a workout example
``> curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises -H "Content-Type: application/json" -d "{\"reps\": 10, \"sets\": 3}"``
## DELETE
``> curl -X DELETE http://localhost:5555/exercises/[ID]`` <br> 
``> curl -X DELETE http://localhost:5555/workouts/[ID]``

