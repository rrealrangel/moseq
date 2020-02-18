#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Nonparametric Standardized Drought Indices - pySDI main script
Author
------
    Roberto A. Real-Rangel (rrealr@iingen.unam.mx)

License
-------
    GNU General Public License
"""
from datetime import datetime as dt

from pysdi import data_manager as dmgr
from pysdi import drought_definition as drgt

config = dmgr.Configurations(config_file='test.toml')

# Check if there is any missing dataset in the import directory.
dmgr.check_source(
    raw_dataset=config.general['input_dir_raw'],
    imp_dataset=config.general['input_dir_imported']
    )

# Load the input indicators (environmental variables).
print("- Opening MERRA-2 datasets.")
indicators = dmgr.xr.open_mfdataset(
    paths=(config.general['input_dir_imported'] + '**/*.nc4'),
    autoclose=True,
    parallel=False
    )
indicators = dmgr.convert_units(indicators)

for temp_scale in config.intensity['temp_scale']:
    for index, variable in config.intensity['sdi'].iteritems():
        # Compute drought intensity.
        drought_intensity = drgt.compute_npsdi(
            data=indicators,
            temp_scale=temp_scale,
            index=index,
            variable=variable,
            output_res=config.general['output_spatial_resolution'],
            nodata=config.general['output_nodata'],
            trim_vmap=config.general['trim_vmap'],
            interp_method=config.general['output_interp_method']
            )
        arrays_to_export = [drought_intensity]

        if (config.magnitude['compute']) and (temp_scale == 1):
            # Compute drought magnitude.
            drought_magnitude = drgt.compute_magnitude(
                intensity=drought_intensity,
                severity_threshold=config.magnitude['intensity_threshold']
                )
            arrays_to_export.append(drought_magnitude)

        # Export results to .nc4 files.
        if config.general['export_last']:
            dates_to_export = [drought_intensity.time[-1].values]

        else:
            dates_to_export = [i.values for i in drought_intensity.time]

        for d, date in enumerate(dates_to_export):
            output_dataset = dmgr.monthly_dataset(
                date=date,
                arrays=arrays_to_export,
                title=(index + '-' + str(temp_scale).zfill(2))
                )
            output_dir = (
                config.general['output_dir'] + '/' + index.lower()
                + str(temp_scale).zfill(2) + '/'
                + str(date).split('-')[0]
                )
            dmgr.export_nc4(
                dataset=output_dataset,
                output_dir=output_dir,
                prefix=config.general['output_fname_prefix']
                )
            dmgr.progress_message(
                current=(d + 1),
                total=len(dates_to_export),
                message="- Exporting results",
                units='files'
                )

print("Process ended at {}.".format(dt.now()))
