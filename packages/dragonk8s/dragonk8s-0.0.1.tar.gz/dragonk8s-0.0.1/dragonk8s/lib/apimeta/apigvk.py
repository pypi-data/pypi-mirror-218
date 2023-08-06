from kubernetes.client.models import v1_controller_revision
from kubernetes.client.models import V1Pod

class GVK(object):

    def __init__(self, group="", version="", kind="", response_type=""):
        self.group = group
        self.version = version
        self.kind = kind
        self.response_type = response_type

    @property
    def group_version(self):
        if self.group != "":
            return "%s/%s" % (self.group, self.version)
        return self.version


def get_resource_client(kube_client, gvk):
    return kube_client.resources.get(api_version=gvk.group_version, kind=gvk.kind)


AppsV1ControllerRevision = GVK(
    group="apps", version="v1", kind="ControllerRevision", response_type="V1ControllerRevision")

IoDragonAppsV1ReplicaSet = GVK(
    group="apps.dragon.io", version="v1", kind="ReplicaSet", response_type="IoDragonAppsV1ReplicaSet")

CoreV1Pod = GVK(
    group="", version="v1", kind="Pod", response_type="V1Pod")

EventsV1Event = GVK(
    group="events.k8s.io", version="v1", kind="Event", response_type="EventsV1Event")

ALL = [AppsV1ControllerRevision, IoDragonAppsV1ReplicaSet, CoreV1Pod, EventsV1Event]
