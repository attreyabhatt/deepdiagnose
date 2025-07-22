from storages.backends.s3boto3 import S3Boto3Storage

def get_signed_url(file_field):
    storage = S3Boto3Storage()
    return storage.url(file_field.name)