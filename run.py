__author__ = 'johnedenfield'

from app import app,db
from app.login.models import User
if __name__ == "__main__":
    db.create_all()
    if User.query.first() is None:
        test =User('test','test')
        db.session.add(test)
        db.session.commit()

    app.run(debug=True)
