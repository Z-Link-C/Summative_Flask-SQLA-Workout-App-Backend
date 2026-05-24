from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id=fields.Integer(dump_only=True)
    name=fields.String(
        required=True,
        validate=validate.Length(min=1,max=255)
    )
    category = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    equipment_needed = fields.Boolean(load_default=False)

    class Meta:
        fields = ('id', 'name', 'category', 'equipment_needed')

class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True,
        validate=validate.Range(min=1)
    )
    notes = fields.String(allow_none=True)
    exercises = fields.List(fields.Nested(ExerciseSchema), dump_only=True)

    class Meta:
        fields = ('id', 'date', 'duration_minutes', 'notes', 'exercises')

class WorkoutExerciseSchema(Schema):
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=1))

    class Meta:
        fields = ('workout_id', 'exercise_id', 'reps', 'sets', 'duration_seconds')    