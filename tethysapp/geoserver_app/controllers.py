import random
import string

from django.shortcuts import render
from tethys_sdk.routing import controller

from tethys_sdk.gizmos import *
from .app import GeoserverApp as app


WORKSPACE = 'geoserver_app'
GEOSERVER_URI = 'http://www.example.com/geoserver-app'


@controller
def home(request):
    """
    Controller for the app home page.
    """
    # Retrieve a geoserver engine
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    # Check for workspace and create workspace for app if it doesn't exist
    response = geoserver_engine.list_workspaces()

    if response['success']:
        workspaces = response['result']

        if WORKSPACE not in workspaces:
            geoserver_engine.create_workspace(workspace_id=WORKSPACE, uri=GEOSERVER_URI)

    # Case where the form has been submitted
    if request.POST and 'submit' in request.POST:
        # Verify files are included with the form
        if request.FILES and 'files' in request.FILES:
            # Get a list of the files
            file_list = request.FILES.getlist('files')

            # Upload shapefile
            store = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            store_id = WORKSPACE + ':' + store
            geoserver_engine.create_shapefile_resource(
                store_id=store_id,
                shapefile_upload=file_list,
                overwrite=True
            )

    context = {}

    return render(request, 'geoserver_app/home.html', context)
