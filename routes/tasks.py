from flask import Blueprint, request, jsonify, abort
from models.task import Task
from models import db, TaskSchema

task_schema = TaskSchema() ##serializer
tasks_schema = TaskSchema(many=True) ##Serializer for many objects

tasks_bp = Blueprint('tasks_bp', __name__)



@tasks_bp.route('/tasks',methods=['GET'])
def get_tasks():
    page = request.args.get('page', 1, type=int) # Get page number from URL; default is 1
    per_page = request.args.get("per_page", 10, type=int)  # Items per page; default is 10
    completed_param = request.args.get('completed')


    if completed_param is not None:
        if completed_param.lower() == 'true':
            query = Task.query.filter(Task.completed.is_(True))
        elif completed_param.lower() == 'false':
            query = Task.query.filter(Task.completed.is_(False))
        else:
            return jsonify({"error": "Invalid value for 'completed'. Use 'true' or 'false'." })
    
    else:
        query = Task.query # fallback if no filtering provided. Used in next line
    
    
    pagination = query.paginate(page=page, per_page=per_page, error_out=False) ##It only fetches the specific page of results — not all of them. This is the task.query.all() setup happening
    tasks = pagination.items
    total = pagination.total

    return jsonify({
        'tasks': tasks_schema.dump(tasks),
        'total_tasks': total,
        'current_page': page,
        'per_page': per_page,
        'total_pages': pagination.pages
    }), 200 #proving response code as second return value. It is good practice to wrap return values in jsonify as it fixes format

@tasks_bp.route('/tasks/<int:id>', methods=['GET'])
def get_task_id(id):
    task = Task.query.get(id) # query.get is outdated in SQLAlchemy so use session
    if not task:
        abort(404, description="Task not Found")
    return task_schema.jsonify(task), 200

@tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
def edit_completed(id):
    task = Task.query.get(id) 
    if not task:
        abort(404, description="Task not Found")

    data = request.get_json()
    if not data or 'completed' not in data:
        abort (400, description="Request Body must contain 'completed field")

    new_val = data['completed'] # getting new val from the body of the request
    
    if type(new_val) is not bool:
        abort(400, description="'Completed' field must be true/false")

    task.completed = new_val #updating task completed to new val in the server
    # db.session.commit() #saving changes in the server

    return task_schema.jsonify(task), 200
    

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    print(data)
    if not 'completed' or 'title' not in data:
        abort(400, description = "Please enter all required data")

    stripped_title = data['title'].strip()
    if len(stripped_title) <= 1 or stripped_title == " ": 
        abort(400, description = "Title cannot be empty or less than 1 character" )
    else: new_title = data['title']
    new_completed = data['completed']

    if type(new_completed) is not bool:
        abort(400, description = " Completed needs to be true or false")

    task = Task(title = new_title, completed = new_completed)
    db.session.add(task)  #The task1 instance is added to the SQLAlchemy session (db.session.add(task1)).
    db.session.commit() #The session changes are committed to the database (db.session.commit()), which executes the SQL INSERT statement.
    db.session.refresh(task)

    return task_schema.jsonify(task), 200

@tasks_bp.route('tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        abort(400, description="Task Not found")
    db.session.delete(task)
    db.session.commit()
    db.session.refresh(task)
    return {"message": "Task Deleted"}, 200


