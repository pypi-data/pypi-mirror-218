import setuptools

api_version = "1.0.0"

api_version_file = "openapi_server/openapi_version"
try:
    with open(api_version_file, 'r') as f:
        val = f.readline().split()
        api_version = ".".join(val)
except OSError:
    print('openapi version file not found')

print(api_version)

# "gunicorn",
# "gevent",
# "flask",
# "flask-limiter",
# "flask-cors",
# "grpcio==1.47.0",
# "grpcio-tools==1.47.0",
# "protobuf==3.20.1",
# "requests",
# "ipaddress",
# "retry",
# "swagger-ui-bundle>=0.0.2",
# "python_dateutil>=2.6.0",
# "connexion[swagger-ui]>=2.6.0; python_version>='3.6'",
# "connexion[swagger-ui]<=2.3.0; python_version=='3.5' or python_version=='3.4'",
# "werkzeug == 0.16.1; python_version=='3.5' or python_version=='3.4'",
# "PyJWT"

setuptools.setup(
    name="openapi_server_test",
    version=api_version,
    author="BD Data Sys IE CDN",
    description="CDN DMS Open API",
    url="https://code.byted.org/savanna/dingman_api_server",
    # package_data={
    #     "": ["openapi_version"],
    # },
    # packages=setuptools.find_packages(where="openapi_server"),
    packages=['openapi_server/test', 'openapi_server/models', 'openapi_server/controllers'],
    # package_dir={"":"openapi_server"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires = [
        "flask"
    ],
)