import random
import string

from tethys_sdk.routing import controller

from tethys_sdk.gizmos import *
from .app import App


WORKSPACE = 'geoserver_app'
GEOSERVER_URI = 'http://www.example.com/geoserver-app'


@controller
def home(request):
    """
    Controller for the app home page.
    """
    breakpoint()
    # Retrieve a geoserver engine
    geoserver_engine = App.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    # Check for workspace and create workspace for app if it doesn't exist
    response = geoserver_engine.list_workspaces()

    if response['success']:
        workspaces = response['result']

        if WORKSPACE not in workspaces:
            from urllib.parse import urlparse
            parsed = urlparse(geoserver_engine.public_endpoint)
            uri = f'{parsed.scheme}://{parsed.netloc}/{WORKSPACE}'
            geoserver_engine.create_workspace(workspace_id=WORKSPACE, uri=uri)

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

    return App.render(request, 'home.html', context)