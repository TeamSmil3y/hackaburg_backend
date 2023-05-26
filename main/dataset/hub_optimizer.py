from ..models import Hub, Company
from django.db.models import Q
from sklearn.cluster import DBSCAN
import numpy as np

threshold = 0.0005 # in rad

hubs = Hub.objects.all()

data_points = np.array([[hub.latitude, hub.longitude] for hub in hubs])

# Create DBSCAN object
dbscan = DBSCAN(eps=threshold, min_samples=1)  # Adjust the threshold value as per your requirement

# Perform clustering
labels = dbscan.fit_predict(data_points)

# Retrieve the unique clusters
unique_labels = np.unique(labels)

# Print the clusters and their corresponding points


new_hubs = []
for label in unique_labels:
    cluster_points = data_points[labels == label]
    latitude, longitude = cluster_points.sum(axis=0)
    hub = Hub(latitude=latitude, longitude=longitude)
    hub.save()
    new_hubs.append(hub)

    for old_latitude, old_longitude in cluster_points:
        h = Hub.objects.filter(latitude=old_latitude, longitude=old_longitude).first()
        for company in Company.objects.filter(hub=h):
            company.hub = hub
            company.save()
        h.delete()

    print(f"Cluster {label}: {cluster_points}")


new_hubs_ids = [i.id for i in new_hubs]

