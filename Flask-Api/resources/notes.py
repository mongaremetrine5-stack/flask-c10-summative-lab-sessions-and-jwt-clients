from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Note


class Notes(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        page = request.args.get("page", 1, type=int)
        per_page = 5

        pagination = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)

        notes = [
            {"id": n.id, "title": n.title, "content": n.content}
            for n in pagination.items
        ]

        return {
            "notes": notes,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        note = Note(
            title=data.get("title"),
            content=data.get("content"),
            user_id=user_id
        )

        db.session.add(note)
        db.session.commit()

        return {"message": "Note created"}, 201


class NoteById(Resource):
    @jwt_required()
    def patch(self, id):
        user_id = get_jwt_identity()

        note = Note.query.filter_by(id=id, user_id=user_id).first()

        if not note:
            return {"error": "Note not found"}, 404

        data = request.get_json()

        note.title = data.get("title", note.title)
        note.content = data.get("content", note.content)

        db.session.commit()

        return {"message": "Note updated"}, 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()

        note = Note.query.filter_by(id=id, user_id=user_id).first()

        if not note:
            return {"error": "Note not found"}, 404

        db.session.delete(note)
        db.session.commit()

        return {"message": "Note deleted"}, 200