# intensity.py
# definitons of intensity characters

from tqdm import tqdm  # progress bar


'''
frequency:
    Calculate frequency (count) of objects in a given radius.

    Formula: count

    Attributes: objects = geoDataFrame with origins
                look_for = geoDataFrame with measured objects (could be the same)
                column_name = name of the column to save calculated values
                id_column = name of column where is stored unique id of each object.
                            If there is none, it could be generated by unique_id().
                radius = radius of buffer zone for calculation. Default is set to 400 (vicinity).
'''


def radius(gpd_df, cpt, radius):
    """
    https://stackoverflow.com/questions/44622233/rtree-count-points-in-the-neighbourhoods-within-each-point-of-another-set-of-po
    :param gpd_df: Geopandas dataframe in which to search for points
    :param cpt:    Point about which to search for neighbouring points
    :param radius: Radius about which to search for neighbours
    :return:       List of point indices around the central point, sorted by
                 distance in ascending order
    """
    # Spatial index
    sindex = gpd_df.sindex
    # Bounding box of rtree search (West, South, East, North)
    bbox = (cpt.x - radius, cpt.y - radius, cpt.x + radius, cpt.y + radius)
    # Potential neighbours
    good = []
    for n in sindex.intersection(bbox):
        dist = cpt.distance(gpd_df['geometry'][n])
        if dist < radius:
            good.append((dist, n))
    # Sort list in ascending order by `dist`, then `n`
    good.sort()
    # Return only the neighbour indices, sorted by distance in ascending order
    return [x[1] for x in good]


def frequency(objects, look_for, column_name, id_column='uID'):
    # define new column

    print('Calculating frequency.')

    objects_centroids = objects.copy()
    objects_centroids['geometry'] = objects_centroids.centroid

    look_for_centroids = objects.copy()
    look_for_centroids['geometry'] = look_for_centroids.centroid

    objects_centroids[column_name] = None
    objects_centroids[column_name] = objects_centroids[column_name].astype('float')

    for index, row in tqdm(objects_centroids.iterrows(), total=objects_centroids.shape[0]):
        neighbours = radius(look_for_centroids, row['geometry'], 400)
        objects.loc[index, column_name] = len(neighbours)

    # objects = objects.merge(objects_centroids[[id_column, column_name]], on=id_column, how='left')

#
# objects = gpd.read_file("/Users/martin/Strathcloud/Personal Folders/Test data/Prague/p7_voro_single.shp")
# column_name = 'test'
# objects
# objects2.head
# objects['geometry'] = objects.centroid
# objects_centroids
