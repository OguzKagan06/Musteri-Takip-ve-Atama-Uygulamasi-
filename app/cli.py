import click
from app import db
from app.models import User

def register_cli_commands(app):
    @app.cli.command('create-admin')
    def create_admin_command():
        """Create a default admin user."""
        user = db.session.scalar(db.select(User).where(User.username == 'admin'))
        if not user:
            admin = User(username='admin', role='admin')
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
