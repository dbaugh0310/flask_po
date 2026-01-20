import unittest
import os
from po_app import app, db
from po_app.models import PO

class ImageIntegrityTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test version of your app
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_visited_po_images_exist(self):
        """Verify that every visited PO has a corresponding physical image file."""
        
        # 1. Define where the images SHOULD be
        # Adjust 'static/images' to match your actual folder structure
        image_dir = os.path.join(self.app.root_path, 'static')
        errors = []
        
        # 2. Query all post offices marked as visited
        visited_pos = db.session.scalars(db.select(PO).where(PO.visited == True)).all()
        
        print(f"\nChecking {len(visited_pos)} images...")

        for po in visited_pos:
            filename = po.po_pic
            
            # Ensure the function actually returned a string
            self.assertIsNotNone(filename, f"PO {po.zip} is visited but po_pic() returned None")
            
            full_path = os.path.join(image_dir, filename)
            if not os.path.exists(full_path):
                errors.append(f"Missing: {filename} (Zip: {po.zip}, City: {po.city})")
            
        if errors:
            self.fail(f"Found {len(errors)} missing images:\n" + "\n".join(errors))

if __name__ == '__main__':
    unittest.main()