from flask import Flask, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import *
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

es = ExerciseSchema()
ess = ExerciseSchema(many=True)
ws = WorkoutSchema()
wss = WorkoutSchema(many=True)
wes = WorkoutExerciseSchema()


@app.route('/exercises', methods=['GET'])
def get_all_exercises():
    exercises = Exercise.query.all()
    return ess.dump(exercises), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    data = es.dump(exercise)
    data['workouts'] = [
        {
            'id': we.workout.id,
            'date': we.workout.date.isoformat(),
            'duration_minutes': we.workout.duration_minutes,
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds
        }
        for we in exercise.workout_exercises
    ]
    return data, 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = es.load(request.json)
        exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return es.dump(exercise), 201
    except ValidationError as err:
        return make_response({'errors': err.messages}, 400)
    except Exception as err:
        db.session.rollback()
        return make_response({'error': str(err)}, 500)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return make_response({'message': 'Exercise deleted'}, 200)
    except Exception as err:
        db.session.rollback()
        return make_response({'error': str(err)}, 500)


@app.route('/workouts', methods=['GET'])
def get_all_workouts():
    workouts = Workout.query.all()
    return wss.dump(workouts), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    data = ws.dump(workout)
    data['workout_exercises'] = [
        {
            'id': we.id,
            'exercise': es.dump(we.exercise),
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds
        }
        for we in workout.workout_exercises
    ]
    return data, 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = ws.load(request.json)
        workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return ws.dump(workout), 201
    except ValidationError as err:
        return make_response({'errors': err.messages}, 400)
    except Exception as err:
        db.session.rollback()
        return make_response({'error': str(err)}, 500)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    try:
        workout = Workout.query.get_or_404(id)
        db.session.delete(workout)
        db.session.commit()
        return make_response({'message': 'Workout deleted'}, 200)
    except Exception as err:
        db.session.rollback()
        return make_response({'error': str(err)}, 500)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        data = request.json or {}

        validated_data = wes.load({
            'workout_id': workout_id,
            'exercise_id': exercise_id,
            'reps': data.get('reps'),
            'sets': data.get('sets'),
            'duration_seconds': data.get('duration_seconds')
        })

        workout = Workout.query.get_or_404(workout_id)
        exercise = Exercise.query.get_or_404(exercise_id)

        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=validated_data.get('reps'),
            sets=validated_data.get('sets'),
            duration_seconds=validated_data.get('duration_seconds')
        )
        db.session.add(we)
        db.session.commit()

        return make_response({'message': 'Exercise added to workout'}, 201)
    except ValidationError as err:
        return make_response({'errors': err.messages}, 400)
    except Exception as err:
        db.session.rollback()
        return make_response({'error': str(err)}, 500)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

