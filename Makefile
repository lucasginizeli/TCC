default: out/lambda.zip

out/lambda.zip: lambda.dockerfile lambda_function.py requirements.txt TCC/settings_try static/staticfiles.json
        mkdir -p out && \
        DOCKER_BUILDKIT=1 docker build -o out -f lambda.dockerfile .

static/staticfiles.json:
        rm -rf static && \
        ../venv/bin/python manage.py collectstatic --no-input

upload-static: static/staticfiles.json
        aws s3 sync static "s3://$(shell cd tf; terraform output -raw static_bucket)/s" \
                --exclude staticfiles.json --delete

.PHONY: default upload-static