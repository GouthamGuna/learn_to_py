import os
import pymongo
from pymongo import MongoClient
from bson.binary import Binary
from datetime import datetime
import argparse
from dotenv import load_dotenv

class ImageUploader:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
    def upload_images(self, image_path):
        """
        Upload all images from the specified path to MongoDB
        """
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        
        # Check if path exists
        if not os.path.exists(image_path):
            print(f"Error: Path '{image_path}' does not exist!")
            return False
        
        uploaded_count = 0
        error_count = 0
        
        # Iterate through all files in the directory
        for filename in os.listdir(image_path):
            file_path = os.path.join(image_path, filename)
            
            # Check if it's a file and has image extension
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                
                if file_ext in image_extensions:
                    try:
                        # Read image file as binary
                        with open(file_path, 'rb') as image_file:
                            image_data = image_file.read()
                        
                        # Create document for MongoDB
                        document = {
                            'filename': filename,
                            'image_data': Binary(image_data),
                            'upload_date': datetime.now(),
                            'file_size': len(image_data),
                            'file_extension': file_ext
                        }
                        
                        # Insert into MongoDB
                        result = self.collection.insert_one(document)
                        
                        print(f"✓ Uploaded: {filename} (ID: {result.inserted_id})")
                        uploaded_count += 1
                        
                    except Exception as e:
                        print(f"✗ Error uploading {filename}: {str(e)}")
                        error_count += 1
        
        print(f"\nUpload completed!")
        print(f"Successfully uploaded: {uploaded_count} images")
        print(f"Errors: {error_count}")
        
        return True
    
    def list_uploaded_images(self):
        """
        List all images currently in the collection
        """
        print("\nImages in collection:")
        print("-" * 50)
        
        images = self.collection.find({}, {'filename': 1, 'upload_date': 1, 'file_size': 1})
        
        for idx, image in enumerate(images, 1):
            print(f"{idx}. {image['filename']} - {image['file_size']} bytes - {image['upload_date']}")
    
    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()

def main():
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    DB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
    DB_NAME = os.getenv('MONGODB_DB_NAME')
    COLLECTION_NAME = os.getenv('MONGODB_COLLECTION')
    IMAGE_PATH = os.getenv('IMAGE_UPLOAD_PATH')
    
    # Validate required environment variables
    if not all([DB_NAME, COLLECTION_NAME, IMAGE_PATH]):
        print("Error: Missing required environment variables. Please check .env file")
        return
    
    # Initialize uploader
    uploader = ImageUploader(DB_URL, DB_NAME, COLLECTION_NAME)
    
    try:
        # Upload images
        print(f"Starting image upload from: {IMAGE_PATH}")
        print(f"Target database: {DB_NAME}.{COLLECTION_NAME}")
        print("-" * 60)
        
        success = uploader.upload_images(IMAGE_PATH)
        
        if success:
            # List uploaded images
            uploader.list_uploaded_images()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Close connection
        uploader.close_connection()

if __name__ == "__main__":
    main()