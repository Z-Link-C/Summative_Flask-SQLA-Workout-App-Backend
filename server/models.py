from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercise', primaryjoin='Exercise.id==WorkoutExercise.exercise_id', secondaryjoin='Workout.id==WorkoutExercise.workout_id', backref='exercises', viewonly=True)

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise name cannot be empty')
        return value.strip()

    @validates('category')
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError('Category cannot be empty')
        return value.strip()


class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        if value is not None and value <= 0:
            raise ValueError('Duration must be greater than 0')
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercise'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
