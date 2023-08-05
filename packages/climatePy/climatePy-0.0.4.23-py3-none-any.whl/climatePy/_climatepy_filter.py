# date, string, misc libraries
from datetime import datetime
import inspect

# spatial libraries
import shapely
import shapely.geometry 
from shapely.ops import transform
import geopandas as gpd
from pyproj import CRS
from rtree import index

# data wrangling and manipulation libraries
import pandas as pd
import numpy as np

# # import climatePy modules
from . import _utils as utils
from . import params

# import climatePy._utils as utils
# from climatePy import params

# warnings lib
import warnings

# suppress warnings
warnings.filterwarnings('ignore', category=Warning)

######## TEST #########
# spoly_wgs84 = gpd.read_file(paths[7])
# spoly_nad83 = gpd.read_file(paths[6])
# # mpoly_wgs84 = gpd.read_file(paths[3])
# # mpoly_nad83 = gpd.read_file(paths[2])
# # spts = gpd.read_file(paths[5])
# mppts = gpd.read_file(paths[1])
# mppts.geometry.tolist()
# mppts.geometry[0].coords.xy
# # AOI = spoly_wgs84
# AOI = spoly_nad83
# AOI = mppts
# AOI = AOI.geometry[0]
# shapely_to_gpd(spoly_wgs84.geometry[0])
# shapely_to_gpd(mppts.geometry[0])
# shapely_to_gpd(spts.geometry[0])
# # type(AOI.geometry
# AOI = [(-105.548, 38.997),(-106.113, 34.407), (-111.67, 39.306)]
# # AOI = [(-105.548, 38.997)]
# AOI = shapely.geometry.MultiPoint(AOI)
# np.asarray(yy).mean()
# AOI.exterior.coords.xy
# # AOI = AOI.geometry
# # AOI = spts
# # AOI = mppts
# # AOI = spoly_nad83
# # id         = "gridmet"
# id = None
# asset      = None
# startDate  = "2023-01-01"
# endDate    = "2023-07-01"
# varname    = ["prcp", "pr", "tmax"]

################################
################################

# Find the maximum bounding box of the AOI
def get_max_bbox(AOI):
    """Find the maximum bounding box of the AOI.

    Args:
        AOI (GeoDataFrame): The area of interest represented as a GeoDataFrame.

    Returns:
        Series: A pandas Series containing the coordinates of the maximum bounding box.
            The Series has the following keys:
                - 'minx': The minimum x-coordinate of the bounding box.
                - 'miny': The minimum y-coordinate of the bounding box.
                - 'maxx': The maximum x-coordinate of the bounding box.
                - 'maxy': The maximum y-coordinate of the bounding box.
    """

    # Calculate the maximum bounding box
    max_bbox = pd.DataFrame({
        'minx': [AOI.bounds['minx'].min()],
        'miny': [AOI.bounds['miny'].min()],
        'maxx': [AOI.bounds['maxx'].max()],
        'maxy': [AOI.bounds['maxy'].max()]
        })
    
    return max_bbox.iloc[0]

def shapely_to_gpd(AOI):

    """Convert a Shapely object to a GeoDataFrame.

    Args:
        AOI (shapely.geometry.base.BaseGeometry): The area of interest as a Shapely object.

    Returns:
        GeoDataFrame: A GeoDataFrame representing the area of interest.
            The GeoDataFrame has a single geometry column with an automatically assigned CRS (either EPSG:4326 or EPSG:5070)

    Note:
        The function assumes that the shapely AOI is in either WGS84 (EPSG:4326) or NAD83 (EPSG:5070) coordinate system.
    """

    # convex hull
    chull = AOI.convex_hull

    # check if convex hull is a point or a polygon
    if isinstance(chull, shapely.geometry.point.Point):
        xx, yy = chull.coords.xy
    else:
        xx, yy = chull.exterior.coords.xy

    # bounding box
    xmax = np.asarray(xx).max()
    xmin = np.asarray(xx).min()
    ymax = np.asarray(yy).max()
    ymin = np.asarray(yy).min()

    # check if AOI is in WGS84 or NAD83
    if (ymax >= -90 and ymax <= 90
        and ymin <= 90 and ymin >= -90
        and xmax >= -180 and xmax <= 180
        and xmin <= 180 and xmin >= -180):
        print("Assuming AOI CRS is EPSG:4326 (WGS84)")
        crs = CRS.from_epsg(4326)
    else:
        print("Assuming AOI CRS is EPSG:5070 (NAD83)")
        crs = CRS.from_epsg(5070)

    out = gpd.GeoDataFrame(geometry = [AOI], crs = crs)

    return out

def find_intersects(catalog, AOI):
    """Check for catalog rows intersecting with the given AOI.

    Args:
        catalog (pandas.DataFrame): A DataFrame containing the catalog information.
        AOI (geopandas.GeoDataFrame): A GeoDataFrame representing the Area of Interest.

    Raises:
        Exception: Raised when no data is found in the provided AOI.

    Returns:
        pandas.DataFrame: A DataFrame containing the intersecting catalog rows.
    """

    # Create an Rtree index of your bounding boxes for each CRS in the catalog
    indexes = {}

    # iterate through unique CRSs and put bounding boxes for each CRS 
    for crs in catalog['crs'].unique():
        
        # RTree index
        idx = index.Index()

        # iterate through catalog rows
        for i, bbox in catalog[catalog['crs']==crs].iterrows():
        
            cat_box = utils.make_vect(cat = bbox)
            
            idx.insert(i, cat_box.geometry.bounds.iloc[0])
            
            indexes[crs] = idx

    # Find which bounding boxes intersect with your AOI using the Rtree index for each CRS
    intersect_lst = []

    # iterate through RTree indexes
    for crs, idx in indexes.items():

        # transform AOI to CRS of bounding box
        AOI_t = AOI.to_crs(crs)

        # get maximum bounding box of AOI
        max_bounds = get_max_bbox(AOI_t)

        # iterate through intersection of transformed AOI and bounding box indexes
        # for i in idx.intersection(AOI_t.bounds.iloc[0]):
        for i in idx.intersection(max_bounds):
            # # catalog row
            # bbox    = catalog.loc[i]
            
            # make bounding box of catalog row
            cat_box = utils.make_vect(cat = catalog.loc[i])
            
            # check if bounding box intersects with the AOI and add to row number to list
            if cat_box.geometry.intersects(AOI_t).any():
                intersect_lst.append(i)

    # get intersecting bounding boxes from catalog
    cat_boxes = catalog.loc[intersect_lst]

    # if no rows are returned after intersection, throw an exception
    if len(cat_boxes) == 0:
        raise Exception("No data found in provided AOI.")
    
    return cat_boxes


def climatepy_filter(
        id         = None,
        asset      = None,
        AOI        = None,
        startDate  = None,
        endDate    = None,
        varname    = None,
        model      = None,
        scenario   = None,
        ensemble   = None
        ):

    """ClimatePy Catalog Filter

        Filter the climatePy catalog based on a set of constraints.

    Args:
        id (str, optional): The resource, agency, or catalog identifier. Defaults to None.
        asset (str, optional): The subdataset or asset in a given resource. Defaults to None.
        AOI (sf object, optional): An sf point or polygon to extract data for. Defaults to None.
        startDate (str, optional): A start date given as "YYYY-MM-DD" to extract data for. Defaults to None.
        endDate (str, optional): An end date given as "YYYY-MM-DD" to extract data for. Defaults to None.
        varname (str, optional): Variable name to extract (e.g. tmin). Defaults to None.
        model (str, optional): GCM model name generating. Defaults to None.
        ensemble (str, optional): The model ensemble member used to generate data. Defaults to None.
        scenario (str, optional): A climate or modeling scenario used. Defaults to None.

    Returns:
        pd.DataFrame: The filtered data frame.
    """

    # initialize variables
    variable, description, duration, e, s, URL = [None]*6

    # if no ID is given, set catalog to all rows of params, otherwise filter down to ID
    if id is None:
        catalog = params()
    else:
        catalog = params()
        catalog = catalog.loc[catalog['id'] == id]
        # catalog = params.loc[params['id'] == id]

    # if no data is found, raise an exception
    if catalog.shape[0] == 0:
        raise Exception('no data to filter.')

    # if asset is given, filter down to asset
    if asset is not None:
        catalog = catalog.loc[catalog['asset'] == asset]
    
    # if no data is found, raise an exception
    if catalog.shape[0] == 0:
        raise Exception('no data to filter.')
    
    # 1. model filter
    if model is not None:

        # unique models
        u = catalog['model'].unique()

        if isinstance(model, str):
            if model not in u:
                bad = model
                m = catalog[['model', 'ensemble']].drop_duplicates()
                message = f"'{bad}' not avaliable model for '{catalog.iloc[0]['id']}'. Try: \n\t{'> ' + m['model'] + ' [' + m['ensemble'] + ']' }"
                raise Exception(message)
            catalog = catalog[catalog['model'].str.contains(model)]
        elif isinstance(model, list):
            if not all(elem in u for elem in model):
                bad = list(set(model) - set(u))
                m = catalog[['model', 'ensemble']].drop_duplicates()
                message = f"'{bad}' not avaliable model for '{catalog.iloc[0]['id']}'. Try: \n\t{'> ' + m['model'] + ' [' + m['ensemble'] + ']' }"
                raise Exception(message)
            catalog = catalog[catalog['model'].str.contains('|'.join(model))]
        # else:
        #     catalog = catalog[catalog['model'].str.contains('|'.join(model))]

    # 2. varname filter 
    if varname is not None:
        
        # make sure varname is a list type
        if isinstance(varname, str):
            varname = [varname]
        
        u = catalog['variable'].unique()
        
        # if all elements in varname are in u, filter down to varname
        if all(elem in u for elem in varname):
            catalog = catalog.loc[catalog['varname'].isin(varname) | catalog['variable'].isin(varname)]
        else:
            bad = list(set(varname) - set(u))
            m = catalog[['variable', 'description', 'units']].drop_duplicates()
            message = f"'{bad}' not avaliable parameter for '{catalog.iloc[0]['id']}'. Try: \n\t{'> ' + m['variable'] + ' [' + m['units'] + '] (' + m['description'] + ')' }"
            raise Exception(message)
    
    # 3.date filter
    if startDate is not None:
        endDate = startDate if endDate is None else endDate
        
        # convert startDate and endDate to datetime
        tmp = (catalog
        .pipe(lambda x: x.assign(s = x['duration'].str.split('/').str[0], 
                                    e = x['duration'].str.split('/').str[1].replace('..', pd.Timestamp.now().strftime('%Y-%m-%d')))
                                    )
        .pipe(lambda x: x.assign(s = pd.to_datetime(x['s'], errors='coerce'),
                                    e = pd.to_datetime(x['e'], errors='coerce'))
                                    )
            .query('e >= @startDate and s <= @endDate')
            .assign(duration_str = lambda x: x['duration'].astype(str) + " [" + x['scenario'] + "]")
            )
        # if no data is found, raise an exception
        if tmp.empty:
            duration_str = "\n\t>".join(tmp['duration_str'])
            raise ValueError(f"Valid Date Range(s) includes: {duration_str}")
        else:
            catalog = tmp.drop(['s', 'e'], axis = 1)
            
    # 4. scenario filter
    if scenario is not None:
        if "historical" in catalog["scenario"].unique():
            scenario = ["historical", scenario]

        if scenario is not None:
            if isinstance(scenario, str):
                catalog = catalog[catalog['scenario'].str.contains(scenario)]
            elif isinstance(scenario, list):
                catalog = catalog[catalog['scenario'].str.contains('|'.join(scenario))]

    # If AOI is a shapely geometry, convert AOI into GeoPandas dataframe 
    if isinstance(AOI, (shapely.geometry.point.Point, 
            shapely.geometry.multipoint.MultiPoint,
            shapely.geometry.linestring.LineString, 
            shapely.geometry.multilinestring.MultiLineString, 
            shapely.geometry.polygon.Polygon, 
            shapely.geometry.multipolygon.MultiPolygon)):
        
        # convert shapely geometry to geopandas dataframe
        AOI = shapely_to_gpd(AOI)

    # 5. AOI filter
    if AOI:
        catalog = find_intersects(
            catalog = catalog,
            AOI     = AOI
            )
        
    # remove duplicates
    catalog = catalog[~catalog.drop(['URL'], axis=1).duplicated()]

    return catalog

# from . import utils, params
# import ._utils as utils
# import utils and params from climatePy
# from climatePy import _utils, params
# from src.climatePy import params
# from src.climatePy import utils

# def find_intersects(catalog, AOI):
#     """Check for catalog rows intersecting with the given AOI.

#     Args:
#         catalog (pandas.DataFrame): A DataFrame containing the catalog information.
#         AOI (geopandas.GeoDataFrame): A GeoDataFrame representing the Area of Interest.

#     Raises:
#         Exception: Raised when no data is found in the provided AOI.

#     Returns:
#         pandas.DataFrame: A DataFrame containing the intersecting catalog rows.
#     """

#     # Create an Rtree index of your bounding boxes for each CRS in the catalog
#     indexes = {}
    
#     # iterate through unique CRSs and put bounding boxes for each CRS 
#     for crs in catalog['crs'].unique():
        
#         # RTree index
#         idx = index.Index()
        
#         # iterate through catalog rows
#         for i, bbox in catalog[catalog['crs']==crs].iterrows():
        
#             cat_box = utils.make_vect(cat = bbox)
            
#             idx.insert(i, cat_box.geometry.bounds.iloc[0])
            
#             indexes[crs] = idx

#     # Find which bounding boxes intersect with your AOI using the Rtree index for each CRS
#     intersect_lst = []
    
#     # iterate through RTree indexes
#     for crs, idx in indexes.items():

#         # transform AOI to CRS of bounding box
#         AOI_t = AOI.to_crs(crs)
        
#         # get maximum bounding box of AOI
#         max_bounds = get_max_bbox(AOI_t)

#         # iterate through intersection of transformed AOI and bounding box indexes
#         for i in idx.intersection(max_bounds):
#         # for i in idx.intersection(AOI_t.bounds.iloc[0]):
        
#             # catalog row
#             bbox    = catalog.loc[i]
            
#             # make bounding box of catalog row
#             cat_box = utils.make_vect(cat = catalog.loc[i])
            
#             # check if bounding box intersects with the AOI and add to row number to list
#             if cat_box.geometry.intersects(AOI_t).any():
#                 intersect_lst.append(i)
        
#     # get intersecting bounding boxes from catalog
#     cat_boxes = catalog.loc[intersect_lst]
    
#     # if no rows are returned after intersection, throw an exception
#     if len(cat_boxes) == 0:
#         raise Exception("No data found in provided AOI.")
    
#     return cat_boxes


# def climatepy_filter(
#         id         = None,
#         asset      = None,
#         AOI        = None,
#         startDate  = None,
#         endDate    = None,
#         varname    = None,
#         model      = None,
#         scenario   = None,
#         ensemble   = None
#         ):

#     """ClimatePy Catalog Filter

#         Filter the climatePy catalog based on a set of constraints.

#     Args:
#         id (str, optional): The resource, agency, or catalog identifier. Defaults to None.
#         asset (str, optional): The subdataset or asset in a given resource. Defaults to None.
#         AOI (sf object, optional): An sf point or polygon to extract data for. Defaults to None.
#         startDate (str, optional): A start date given as "YYYY-MM-DD" to extract data for. Defaults to None.
#         endDate (str, optional): An end date given as "YYYY-MM-DD" to extract data for. Defaults to None.
#         varname (str, optional): Variable name to extract (e.g. tmin). Defaults to None.
#         model (str, optional): GCM model name generating. Defaults to None.
#         ensemble (str, optional): The model ensemble member used to generate data. Defaults to None.
#         scenario (str, optional): A climate or modeling scenario used. Defaults to None.

#     Returns:
#         pd.DataFrame: The filtered data frame.
#     """

#     # initialize variables
#     variable, description, duration, e, s, URL = [None]*6

#     # if no ID is given, set catalog to all rows of params, otherwise filter down to ID
#     if id is None:
#         catalog = params()
#     else:
#         catalog = params()
#         catalog = catalog.loc[catalog['id'] == id]
#         # catalog = params.loc[params['id'] == id]

#     # if no data is found, raise an exception
#     if catalog.shape[0] == 0:
#         raise Exception('no data to filter.')

#     # if asset is given, filter down to asset
#     if asset is not None:
#         catalog = catalog.loc[catalog['asset'] == asset]
    
#     # if no data is found, raise an exception
#     if catalog.shape[0] == 0:
#         raise Exception('no data to filter.')
    
#     # 1. model filter
#     if model is not None:

#         # unique models
#         u = catalog['model'].unique()

#         if isinstance(model, str):
#             if model not in u:
#                 bad = model
#                 m = catalog[['model', 'ensemble']].drop_duplicates()
#                 message = f"'{bad}' not avaliable model for '{catalog.iloc[0]['id']}'. Try: \n\t{'> ' + m['model'] + ' [' + m['ensemble'] + ']' }"
#                 raise Exception(message)
#             catalog = catalog[catalog['model'].str.contains(model)]
#         elif isinstance(model, list):
#             if not all(elem in u for elem in model):
#                 bad = list(set(model) - set(u))
#                 m = catalog[['model', 'ensemble']].drop_duplicates()
#                 message = f"'{bad}' not avaliable model for '{catalog.iloc[0]['id']}'. Try: \n\t{'> ' + m['model'] + ' [' + m['ensemble'] + ']' }"
#                 raise Exception(message)
#             catalog = catalog[catalog['model'].str.contains('|'.join(model))]
#         # else:
#         #     catalog = catalog[catalog['model'].str.contains('|'.join(model))]

#     # 2. varname filter 
#     if varname is not None:
        
#         # make sure varname is a list type
#         if isinstance(varname, str):
#             varname = [varname]
        
#         u = catalog['variable'].unique()
        
#         # if all elements in varname are in u, filter down to varname
#         if all(elem in u for elem in varname):
#             catalog = catalog.loc[catalog['varname'].isin(varname) | catalog['variable'].isin(varname)]
#         else:
#             bad = list(set(varname) - set(u))
#             m = catalog[['variable', 'description', 'units']].drop_duplicates()
#             message = f"'{bad}' not avaliable parameter for '{catalog.iloc[0]['id']}'. Try: \n\t{'> ' + m['variable'] + ' [' + m['units'] + '] (' + m['description'] + ')' }"
#             raise Exception(message)
    
#     # 3.date filter
#     if startDate is not None:
#         endDate = startDate if endDate is None else endDate
        
#         # convert startDate and endDate to datetime
#         tmp = (catalog
#         .pipe(lambda x: x.assign(s = x['duration'].str.split('/').str[0], 
#                                     e = x['duration'].str.split('/').str[1].replace('..', pd.Timestamp.now().strftime('%Y-%m-%d')))
#                                     )
#         .pipe(lambda x: x.assign(s = pd.to_datetime(x['s'], errors='coerce'),
#                                     e = pd.to_datetime(x['e'], errors='coerce'))
#                                     )
#             .query('e >= @startDate and s <= @endDate')
#             .assign(duration_str = lambda x: x['duration'].astype(str) + " [" + x['scenario'] + "]")
#             )
#         # if no data is found, raise an exception
#         if tmp.empty:
#             duration_str = "\n\t>".join(tmp['duration_str'])
#             raise ValueError(f"Valid Date Range(s) includes: {duration_str}")
#         else:
#             catalog = tmp.drop(['s', 'e'], axis = 1)
            
#     # 4. scenario filter
#     if scenario is not None:
#         if "historical" in catalog["scenario"].unique():
#             scenario = ["historical", scenario]

#         if scenario is not None:
#             if isinstance(scenario, str):
#                 catalog = catalog[catalog['scenario'].str.contains(scenario)]
#             elif isinstance(scenario, list):
#                 catalog = catalog[catalog['scenario'].str.contains('|'.join(scenario))]

#     # 5. AOI filter
#     if AOI is not None:
#         catalog = find_intersects(
#             catalog = catalog,
#             AOI     = AOI
#             )
        
#     # remove duplicates
#     catalog = catalog[~catalog.drop(['URL'], axis=1).duplicated()]

#     return catalog