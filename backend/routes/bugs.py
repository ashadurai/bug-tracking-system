from flask import Blueprint, request, jsonify
from extensions import db
from models import Bug, Notification

bugs_bp = Blueprint('bugs', __name__)

# GET all bugs
@bugs_bp.route('/', methods=['GET'])
def get_bugs():
    severity = request.args.get('severity')
    status = request.args.get('status')

    query = Bug.query
    if severity: query = query.filter_by(severity=severity)
    if status: query = query.filter_by(status=status)

    bugs = query.order_by(Bug.created_at.desc()).all()
    return jsonify({'bugs': [b.to_dict() for b in bugs], 'count': len(bugs)})

# GET single bug
@bugs_bp.route('/<int:bug_id>', methods=['GET'])
def get_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    return jsonify(bug.to_dict())

# POST create bug
@bugs_bp.route('/', methods=['POST'])
def create_bug():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('severity'):
        return jsonify({'error': 'Title and severity are required'}), 400

    bug = Bug(
        title=data['title'],
        description=data.get('description'),
        steps_to_reproduce=data.get('steps_to_reproduce'),
        expected_behavior=data.get('expected_behavior'),
        actual_behavior=data.get('actual_behavior'),
        severity=data['severity'],
        status=data.get('status', 'Open'),
        project_id=data.get('project_id'),
        assigned_to=data.get('assigned_to'),
        created_by=data.get('created_by')
    )
    db.session.add(bug)
    db.session.flush()

    # Send notification to assigned user
    if bug.assigned_to:
        notification = Notification(
            user_id=bug.assigned_to,
            message=f'You have been assigned a new bug: {bug.title}'
        )
        db.session.add(notification)

    db.session.commit()
    return jsonify({'message': 'Bug reported successfully', 'bug': bug.to_dict()}), 201

# PUT update bug status
@bugs_bp.route('/<int:bug_id>', methods=['PUT'])
def update_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    data = request.get_json()
    if data.get('title'): bug.title = data['title']
    if data.get('severity'): bug.severity = data['severity']
    if data.get('status'): bug.status = data['status']
    if data.get('assigned_to'): bug.assigned_to = data['assigned_to']
    db.session.commit()
    return jsonify({'message': 'Bug updated successfully', 'bug': bug.to_dict()})

# DELETE bug
@bugs_bp.route('/<int:bug_id>', methods=['DELETE'])
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()
    return jsonify({'message': 'Bug deleted successfully'})

# GET bug stats
@bugs_bp.route('/stats/summary', methods=['GET'])
def bug_stats():
    total = Bug.query.count()
    open_bugs = Bug.query.filter_by(status='Open').count()
    in_progress = Bug.query.filter_by(status='In Progress').count()
    resolved = Bug.query.filter_by(status='Resolved').count()
    closed = Bug.query.filter_by(status='Closed').count()
    critical = Bug.query.filter_by(severity='Critical').count()
    high = Bug.query.filter_by(severity='High').count()
    medium = Bug.query.filter_by(severity='Medium').count()
    low = Bug.query.filter_by(severity='Low').count()

    return jsonify({
        'total': total,
        'by_status': {'open': open_bugs, 'in_progress': in_progress, 'resolved': resolved, 'closed': closed},
        'by_severity': {'critical': critical, 'high': high, 'medium': medium, 'low': low}
    })
