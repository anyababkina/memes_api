example_responses_create = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {"message": f"Successfully uploaded file.file to S3", "url": "s3/file.png"}
            }
        }
    },

    400: {
        'description': 'Something wrong in S3',
        'content': {
            'application/json': {
                'example': {'detail': 'Something went wrong in S3 server'}
            }
        }
    }
}

example_responses_delete = {
    200: {
        "description": "Successful response",
        "content": {
            "application/json": {
                "example": {"message": f"Successfully deleted 'file.png' from S3"}
            }
        }
    },

    400: {
        'description': 'Something wrong in S3',
        'content': {
            'application/json': {
                'example': {'detail': 'Something went wrong in S3 server'}
            }
        }
    }
}


example_responses_get = {
    404: {
        "description": "File not found",
        "content": {
            "application/json": {
                "example": {"detail": "File not found"}
            }
        }
    },

    400: {
        'description': 'Something wrong in S3',
        'content': {
            'application/json': {
                'example': {'detail': 'Something went wrong in S3 server'}
            }
        }
    }
}