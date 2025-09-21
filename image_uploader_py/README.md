# Image Uploader

This project provides a Python-based utility for uploading and managing images. It's designed to handle images from medical camps and similar scenarios where bulk image management is required.

## Environment Setup

The application uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

```env
MONGODB_URL=mongodb://localhost:27017/    # MongoDB connection URL
MONGODB_DB_NAME=your_db_name             # Database name
MONGODB_COLLECTION=your_collection       # Collection name for storing images
IMAGE_UPLOAD_PATH=/path/to/images       # Path to the directory containing images
```

**Important:** Never commit the `.env` file to version control. A `.env.example` file is provided as a template.

## Features

- Bulk image upload support
- Medical camp image organization
- Support for common image formats (JPEG, PNG)
- Directory-based image management

## Project Structure

- `image_uploader.py` - Main script for image upload functionality
- `xyz/` - Directory containing xyz images
- `requirements.txt` - Python dependencies file

## Use virtual environments for projects

```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\Scripts\activate
```

## Uninstall All Packages from requirements.txt

```bash
pip uninstall -r requirements.txt -y
```

## Recreate the Virtual Environment (Recommended)

```bash
# Deactivate current environment (if active)
deactivate

# Remove the broken virtual environment
Remove-Item -Recurse -Force .venv

# Create new virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\activate

# Now install requirements
pip install -r requirements.txt
```
