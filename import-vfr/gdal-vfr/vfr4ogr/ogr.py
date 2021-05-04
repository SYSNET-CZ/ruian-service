import datetime
import mimetypes
import os
import sys
import time

from utils3 import fatal, message, download_vfr, last_day_of_month, yesterday, logger

CUZAK_VFR_SOUCASNA = 'http://vdp.cuzk.cz/vymenny_format/soucasna/'

try:
    from osgeo import gdal, ogr
except ImportError as e:
    sys.exit('ERROR: Import of ogr from osgeo failed. %s' % e)


# redirect warnings to the file
def error_handler(err_level, err_no, err_msg):
    if err_no is not None:
        err_msg = '['+err_no+'] ' + err_msg
    if err_level > gdal.CE_Warning:
        raise RuntimeError(err_msg)
    elif err_level == gdal.CE_Debug:
        sys.stderr.write(err_msg + os.linesep)
    else:
        logger.warning(err_msg)


# check GDAL/OGR library, version >= 1.11 required
def check_ogr():
    # check required version
    version = gdal.__version__.split('.', 1)
    if not (int(version[0]) > 1 or int(version[1].split('.', 1)[0]) >= 11):
        fatal("GDAL/OGR 1.11 or later required (%s found)" % '.'.join(version))

    # check if OGR comes with GML driver
    if not ogr.GetDriverByName('GML'):
        fatal('GML driver required')

    gdal.PushErrorHandler(error_handler)


# open VFR file for reading
def open_file(filename, download=True, force_date=None):
    drv = ogr.GetDriverByName("GML")
    if drv is None:
        fatal("Unable to select GML driver")
    list_ds = list()
    if os.linesep in filename:
        # already list of files (date range)
        return filename.split(os.linesep)

    if mimetypes.guess_type(filename)[0] == 'text/plain':
        # list of files given as text file
        f = None
        try:
            f = open(filename)
            i = 0
            lines = f.read().splitlines()
            for line in lines:
                if len(line) < 1 or line.startswith('#'):
                    continue  # skip empty or commented lines

                if not line.startswith('http://') and \
                        not line.startswith('20'):
                    # determine date if missing
                    if not force_date:
                        if line.startswith('ST_Z'):
                            date = yesterday()
                        else:
                            date = last_day_of_month()
                    else:
                        date = force_date
                    line = date + '_' + line

                if not line.endswith('.xml.gz'):
                    # add extension if missing
                    line += '.xml.gz'

                if not os.path.exists(line):
                    if not line.startswith('http://'):
                        line = CUZAK_VFR_SOUCASNA + line
                    if download:
                        line = download_vfr(line)

                list_ds.append(line)
                i += 1
            message("%d VFR files will be processed..." % len(list_ds))
        except IOError:
            fatal("Unable to read '%s'" % filename)
        f.close()
    else:
        # single VFR file
        list_ds.append(filename)

    return list_ds


# open OGR data-source for reading
def open_ds(filename):
    drv = ogr.GetDriverByName("GML")
    ds = drv.Open(filename, False)
    if ds is None:
        sys.stderr.write("File '%s' not found. Skipping.\n" % filename)

    return ds


# list supported OGR formats
def list_formats():
    cnt = ogr.GetDriverCount()

    formatsList = []
    for i in range(cnt):
        driver = ogr.GetDriver(i)
        if not driver.TestCapability("CreateDataSource"):
            continue
        driverName = driver.GetName()
        if driverName == 'GML':
            continue

        formatsList.append(driverName.replace(' ', '_'))

    for i in sorted(formatsList):
        print(i)


# get list of geometry column for specified layer
def get_geom_count(layer):
    defn = layer.GetLayerDefn()
    geom_list = list()
    for i in range(defn.GetGeomFieldCount()):
        geom_list.append([defn.GetGeomFieldDefn(i).GetName(), 0])

    for feature in layer:
        for i in range(len(geom_list)):
            if feature.GetGeomFieldRef(i):
                geom_list[i][1] += 1

    return geom_list


# list OGR layers of input VFR file
def list_layers(ds, extended=False, fd=sys.stdout):
    nlayers = ds.GetLayerCount()
    layer_list = list()
    for i in range(nlayers):
        layer = ds.GetLayer(i)
        layerName = layer.GetName()
        layer_list.append(layerName)

        if not fd:
            continue

        if extended:
            fd.write('-' * 80 + os.linesep)
        featureCount = layer.GetFeatureCount()
        fd.write("Number of features in %-20s: %d\n" % (layerName, featureCount))
        if extended:
            for field, count in get_geom_count(layer):
                fd.write("%41s : %d\n" % (field, count))

    if fd:
        fd.write('-' * 80 + os.linesep)

    return layer_list


# print summary for multiple file input
def print_summary(odsn, frmt, layer_list, stime):
    odrv = ogr.GetDriverByName(frmt)
    if odrv is None:
        fatal("Format '%s' is not supported" % frmt)

    ods = odrv.Open(odsn, False)
    if ods is None:
        return
    # fatal("Unable to open datasource '%s'" % odsn)

    message("Summary")
    for layer_name in layer_list:
        layer = ods.GetLayerByName(layer_name)
        if not layer:
            continue

        sys.stdout.write("Layer            %-20s ... %10d features\n" % (layer_name, layer.GetFeatureCount()))

    nsec = time.time() - stime
    etime = str(datetime.timedelta(seconds=nsec))
    message("Time elapsed: %s" % str(etime))

    ods.Destroy()
