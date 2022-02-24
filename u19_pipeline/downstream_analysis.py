import datajoint as dj
from u19_pipeline.imaging_element import imaging_element
# import logging

# logger = logging.getLogger(__name__)

schema = dj.schema(dj.config['custom']['database.prefix'] + 'downstream_analysis', locals())

@schema
class DownstreamActivityAnalysis(dj.Computed):
    definition = """ # versions for the meso pipeline
    -> imaging_element.Activity.Trace
    ---
    mean: float    # mean activity
    stdev: float   # standard deviation of activity
    max: float     # maximum activity
    """
    def make(self, key):
        mask_ids = (imaging_element.Activity.Trace() & key).fetch("mask")
        for mask_id in mask_ids:
            trace = (imaging_element.Activity.Trace() & key & dict(mask=mask_id)).fetch1("activity_trace")

            # compute various statistics on activity
            key['mean'] = trace.mean()  # compute mean
            key['stdev'] = trace.std()  # compute standard deviation
            key['max'] = trace.max()    # compute max
            self.insert1(key, skip_duplicates=True)