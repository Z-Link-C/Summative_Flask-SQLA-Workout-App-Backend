from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


WorkoutExercises = db.Table(
    'workout_exercises',
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id')),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id')),
    db.Column('reps', db.Integer),
    db.Column('sets', db.Integer),
    db.Column('duration_seconds', db.Integer)
)


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    workouts = db.relationship('Workout', secondary=WorkoutExercises, back_populates='exercises')

    @validates('name')
    def validate_name(self, val):
        if not val or not val.strip():
            raise ValueError('Exercise name cannot be empty')
        return val.strip()

    @validates('category')
    def validate_category(self, val):
        if not val or not val.strip():
            raise ValueError('Category cannot be empty')
        return val.strip()


class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    exercises = db.relationship('Exercise', secondary=WorkoutExercises, back_populates='workouts')

    @validates('date')
    def validate_date(self, val):
        if val > datetime.now().date():
            raise ValueError('Workout date cannot be in the future')
        return val

    @validates('duration_minutes')
    def validate_duration_minutes(self, val):
        if val is not None and val <= 0:
            raise ValueError('Duration must be greater than 0')
        return val
