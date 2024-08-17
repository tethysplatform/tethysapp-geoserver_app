from tethys_sdk.base import TethysAppBase
from tethys_sdk.app_settings import SpatialDatasetServiceSetting

class App(TethysAppBase):
    """
    Tethys app class for Geoserver App.
    """
    name = 'Geoserver App'
    description = ''
    package = 'geoserver_app'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'geoserver-app'
    color = '#d35400'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def spatial_dataset_service_settings(self):
        """
        Example spatial_dataset_service_settings method.
        """
        sds_settings = (
            SpatialDatasetServiceSetting(
                name='main_geoserver',
                description='spatial dataset service for app to use',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )

        return sds_settings
