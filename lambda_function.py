import lambda_venv_path  # noqa


def hello(event, context):
    """Entry point for minimal testing"""
    if event.get('install_secrets'):
        install_secrets()

    return {
        'message': 'Hello from the Wagtail Lambda Demo',
        'event': event,
        'context': repr(context),
    }


def install_secrets():
    """Add the secrets from the secret named by ENV_SECRET_ID to os.environ"""
    import os
    secret_id = os.environ.get('ENV_SECRET_ID')
    if not secret_id:
        return

    import boto3
    import json

    session = boto3.session.Session()
    client = session.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_id)
    overlay = json.loads(response['SecretString'])
    os.environ.update(overlay)


def manage(event, context):
    """Entry point for running a management command. Supported formats:

    - "migrate"
    - ["migrate"]
    - {"command": ["migrate"]}
    """
    if isinstance(event, dict):
        command = event['command']
    else:
        command = event
    if isinstance(command, str):
        command = command.split()

    install_secrets()
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()  # Initialize Django
    from django.core import management
    return management.call_command(*command)


_real_handler = None


def lambda_handler(event, context):
    """Entry point for web requests"""
    global _real_handler

    if _real_handler is None:
        install_secrets()

        from apig_wsgi import make_lambda_handler
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        _real_handler = make_lambda_handler(application)

    return _real_handler(event, context)

