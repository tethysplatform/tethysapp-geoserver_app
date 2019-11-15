import random
import string

from django.shortcuts import render
from tethys_sdk.permissions import login_required

from tethys_sdk.gizmos import *
from .app import GeoserverApp as app


WORKSPACE = 'geoserver_app'
GEOSERVER_URI = 'http://www.example.com/geoserver-app'


@login_required()
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


@login_required()
def map(request):
    """
    Controller for the map page
    """
    geoserver_engine = app.get_spatial_dataset_service(name='main_geoserver', as_engine=True)

    options = []

    response = geoserver_engine.list_layers(with_properties=False)

    if response['success']:
        for layer in response['result']:
            options.append((layer.title(), layer))

    select_options = SelectInput(
        display_text='Choose Layer',
        name='layer',
        multiple=False,
        options=options
    )

    map_layers = []

    if request.POST and 'layer' in request.POST:
        selected_layer = request.POST['layer']
        legend_title = selected_layer.title()

        geoserver_layer = MVLayer(
            source='ImageWMS',
            options={
                'url': 'http://localhost:8181/geoserver/wms',
                'params': {'LAYERS': selected_layer},
                'serverType': 'geoserver'
            },
            legend_title=legend_title,
            legend_extent=[-114, 36.5, -109, 42.5],
            legend_classes=[
                MVLegendClass('polygon', 'County', fill='#999999'),
        ])

        map_layers.append(geoserver_layer)


    view_options = MVView(
        projection='EPSG:4326',
        center=[-100, 40],
        zoom=4,
        maxZoom=18,
        minZoom=2
    )

    map_options = MapView(
        height='500px',
        width='100%',
        layers=map_layers,
        legend=True,
        view=view_options
    )

    context = {'map_options': map_options,
               'select_options': select_options}

    return render(request, 'geoserver_app/map.html', context)


@login_required()
def draw(request):
    drawing_options = MVDraw(
        controls=['Modify', 'Move', 'Point', 'LineString', 'Polygon', 'Box'],
        initial='Polygon'
    )

    map_options = MapView(
        height='450px',
        width='100%',
        layers=[],
        draw=drawing_options
    )

    geometry = ''

    if request.POST and 'geometry' in request.POST:
        geometry = request.POST['geometry']

    context = {'map_options': map_options,
               'geometry': geometry}

    return render(request, 'geoserver_app/draw.html', context)
