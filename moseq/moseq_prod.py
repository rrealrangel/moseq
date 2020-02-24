# -*- coding: utf-8 -*-
"""Nonparametric Standardized Drought Indices - pySDI main script
Author
------
    Roberto A. Real-Rangel (Institute of Engineering UNAM; Mexico)

License
-------
    GNU General Public License
"""
import datetime as dt

from droughtMoPro import data_manager as dmgr
from droughtMoPro import maps_pgdi as pgdi
from droughtMoPro import maps_sdi as maps
from droughtMoPro import reports as rep
from droughtMoPro import time_series as ts

run_start = dt.datetime.now()
print("---- Process started at {start} ----".format(start=run_start))
settings = dmgr.Configurations(config_file='test.toml')

# Export drought intensity maps to KML format files.
if settings.intensity_maps['export']:
    print("- Working on drought intensity maps.")

    # Available source data to generate drought monitoring products.
    data_files = dmgr.list_files(
        parent_dir=settings.general['input_data_dir'],
        pattern=settings.intensity_maps['input_data_fpatt'],
        what=settings.intensity_maps['output_period_to_export']
        )

    for df, data_file in enumerate(data_files):
        maps.export_dint(
            input_file=str(data_file),
            output_dir=settings.intensity_maps['output_dir'],
            nodata=settings.general['NODATA'],
            output_fname_prefix=settings.general['output_prefix'],
            overwrite=settings.general['overwrite']
            )
        dmgr.progress_message(
            current=(df + 1),
            total=len(data_files),
            message="- Exporting the drought intensity maps",
            units='maps'
            )

# Export drought magnitude maps to KML format files.
if settings.magnitude_maps['export']:
    print("- Working on drought magnitude maps.")

    # Available source data to generate drought monitoring products.
    data_files = dmgr.list_files(
        parent_dir=settings.general['input_data_dir'],
        pattern=settings.magnitude_maps['input_data_fpatt'],
        what=settings.magnitude_maps['output_period_to_export']
        )

    for df, data_file in enumerate(data_files):
        maps.export_dmag(
            input_file=str(data_file),
            output_dir=settings.magnitude_maps['output_dir'],
            nodata=settings.general['NODATA'],
            output_fname_prefix=settings.general['output_prefix'],
            overwrite=settings.general['overwrite']
            )
        dmgr.progress_message(
            current=(df + 1),
            total=len(data_files),
            message="- Exporting the drought magnitude maps",
            units='maps'
            )

# Export time series.
if settings.time_series['export']:
    print("- Working on time series products.")
    data_files = dmgr.list_files(
        parent_dir=settings.general['input_data_dir'],
        pattern=settings.time_series['input_data_fpatt'],
        what=settings.time_series['output_period_to_export']
        )
    map_files = dmgr.list_files(
        parent_dir=settings.time_series['input_vmaps_dir'],
        pattern=settings.time_series['input_mapfile_patt']
        )
    ts.export_ts(
        data_files=[str(i) for i in data_files],
        map_files=map_files,
        nodata=settings.general['NODATA'],
        output_dir=settings.time_series['output_dir']
        )

# Export reports.
if settings.reports['export']:
    print("- Working on drought reports.")
    print("    - Reading regions maps.")
    data_files = dmgr.list_files(
        parent_dir=settings.general['input_data_dir'],
        pattern=settings.reports['input_data_fpatt'],
        what=settings.reports['output_period_to_export']
        )
    map_files = dmgr.list_files(
        parent_dir=settings.time_series['input_vmaps_dir'],
        pattern=settings.reports['input_mapfile_patt']
        )
    rep.make_report(
        data_files=[str(i) for i in data_files],
        map_files=map_files,
        output_dir=settings.reports['output_dir'],
        nodata=settings.general['NODATA']
        )

# Compute and export Proxy groundwater drought index (PGDI)
# TODO: Apply the PGDI filter to the SDI files with the original resolution.
if settings.pgdi_maps['export']:
    print("- Working on the Proxy Groundwater Drought Index maps.")
    data_files = dmgr.list_files(
        parent_dir=settings.pgdi_maps['input_data_dir'],
        pattern=settings.pgdi_maps['input_data_fpatt'],
        what=settings.pgdi_maps['output_period_to_export']
        )
    pgdi.export_pgdi_maps(
        data_files=[str(i) for i in data_files],
        filter_file=settings.pgdi_maps['input_filter_fpath'],
        trim_vmap=settings.pgdi_maps['input_trim_vmap'],
        output_res=settings.pgdi_maps['OUTPUT_RES'],
        output_dir=settings.pgdi_maps['output_dir'],
        nodata=settings.general['NODATA']
        )

run_end = dt.datetime.now()
print("---- Process ended at {end}. Time elapsed: {eltime} ----".format(
    end=run_end,
    eltime=str(run_end - run_start)
    ))
