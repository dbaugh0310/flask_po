from po_app import app, db
from po_app.models import PO
import sqlalchemy as sa
import sqlalchemy.orm as so
import json

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'PO': PO}

@app.cli.command("load-json")
def load_json():
    with open('po_data/po.json', 'r') as f:
        data = json.load(f)
        for item in data:
            # Convert 'y' to True, and anything else (like 'n') to False
            if item['visited'] == 'y':
                item['visited'] = True
            else:
                item['visited'] = False
            record = PO(**item)
            db.session.add(record)
        db.session.commit()
    print("Done!")
    
    