from flask import Blueprint, request, jsonify
from extensions import db
from models import Notification

notifications_bp = Blueprint('notifications', __name__)

# GET all notifications for a user
@notifications_bp.route('/user/<int:user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = Notification.query.filter_by(user_id=user_id)\
        .order_by(Notification.created_at.desc()).all()
    return jsonify({
        'notifications': [n.to_dict() for n in notifications],
        'unread_count': sum(1 for n in notifications if not n.is_read)
    })

# PUT mark notification as read
@notifications_bp.route('/<int:notif_id>/read', methods=['PUT'])
def mark_read(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    notif.is_read = True
    db.session.commit()
    return jsonify({'message': 'Notification marked as read'})

# PUT mark all as read
@notifications_bp.route('/user/<int:user_id>/read-all', methods=['PUT'])
def mark_all_read(user_id):
    Notification.query.filter_by(user_id=user_id, is_read=False)\
        .update({'is_read': True})
    db.session.commit()
    return jsonify({'message': 'All notifications marked as read'})
