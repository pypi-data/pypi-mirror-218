from ursactl.core.services import client
from ursactl.core._base import Base


class Project(Base):
    """
    Provides access to a project and its related resources.
    """
    @property
    def client(self):
        if self._client is None:
            self._client = client('usage', self.app)
        return self._client

    @property
    def name(self):
        return self._data['name']

    @property
    def description(self):
        return self._data['description']

    @property
    def is_closed(self):
        return self._data['isClosed']

    def Dataset(self, *args, **kwargs):
        from ursactl.core.dataset import Dataset as DatasetClass

        return DatasetClass(*args, project_uuid=self.uuid, **kwargs)

    def datasets(self):
        """
        Returns a generator listing all datasets belonging to the project.
        """
        from ursactl.core.dataset import Dataset

        if self.uuid is None:
            return []
        dss_client = client('dss', self.app)
        return (
            Dataset(client=dss_client, app=self.app, **info)
            for info in dss_client.list_datasets(project_scope=self.uuid)
        )

    @property
    def _data(self):
        if self._cached_data is None:
            if self.uuid is None:
                self._cached_data = {
                    'name': None,
                    'description': None,
                    'isClosed': None
                }
            else:
                self._cached_data = self.client.get_dataset_details(self.uuid)
        return self._cached_data
