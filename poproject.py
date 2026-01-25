from po_app import app, db
from po_app.models import PO, User
import sqlalchemy as sa
import sqlalchemy.orm as so
import json
import click

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'PO': PO}

@app.cli.command("load-json")
def load_json():
    with open('data/po.json', 'r') as f:
        data = json.load(f)
        for item in data:
            existing = PO.query.filter_by(zip=item['zip']).first()
            if existing:
                continue
            
            item['state'] = item['state'].strip()
            # Convert 'y' to True, and anything else (like 'n') to False
            if item['visited'] == 'y':
                item['visited'] = True
            else:
                item['visited'] = False
            
            record = PO(**item)
            db.session.add(record)
            
        db.session.commit()
    print("Done!")
    
@app.cli.command("set-password")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="The password for the user.")
def set_pass(password):
    user = db.session.scalar(sa.select(User).where(User.username == 'justin'))
    
    if user is None:
        click.echo(f"Initializing account: {'justin'}...")
        user = User(username='justin')
        db.session.add(user) # Tell SQLAlchemy to track this brand-new object
    else:
        click.echo(f"Updating existing account: {'justin'}...")
    
    user.set_password(password)
    db.session.commit()
    click.echo("Admin password updated successfully.")

    
    