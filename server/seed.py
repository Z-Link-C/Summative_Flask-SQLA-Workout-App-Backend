#!/usr/bin/env python3

from app import app
from models import *
from datetime import date

with app.app_context():
    # Reset data - drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Add example exercises
    exercise1 = Exercise(name='Push-ups', category='Upper Body', equipment_needed=False)
    exercise2 = Exercise(name='Squats', category='Lower Body', equipment_needed=False)
    exercise3 = Exercise(name='Bench Press', category='Upper Body', equipment_needed=True)
    exercise4 = Exercise(name='Running', category='Cardio', equipment_needed=False)

    db.session.add_all([exercise1, exercise2, exercise3, exercise4])
    db.session.commit()

    # Add example workouts
    workout1 = Workout(date=date(2024, 1, 15), duration_minutes=45, notes='Morning workout')
    workout2 = Workout(date=date(2024, 1, 16), duration_minutes=60, notes='Leg day')
    workout3 = Workout(date=date(2024, 1, 17), duration_minutes=30, notes='Cardio session')

    db.session.add_all([workout1, workout2, workout3])
    db.session.commit()

    # Add example workout_exercises
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise1.id, reps=20, sets=3)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=exercise3.id, reps=10, sets=4)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=exercise2.id, reps=15, sets=3)
    we4 = WorkoutExercise(workout_id=workout3.id, exercise_id=exercise4.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print('Database seeded successfully!')
    print(f'Added 4 exercises')
    print(f'Added 3 workouts')
    print(f'Added 4 workout_exercises')