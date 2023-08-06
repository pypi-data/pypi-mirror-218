from pyrecdp.primitives.generators import *
from pyrecdp.primitives.profilers import *
from .BasePipeline import BasePipeline
import logging
from pyrecdp.core.dataframe import DataFrameAPI
from pyrecdp.core import SeriesSchema
import pandas as pd
import copy

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.ERROR, datefmt='%I:%M:%S')
logger = logging.getLogger(__name__)

class FeatureWrangler(BasePipeline):
    def __init__(self, dataset, label, *args, **kwargs):
        super().__init__(dataset, label)
        self.data_profiler = [cls() for cls in feature_infer_list]
        # If we provided multiple datasets in this workload
        self.generators.append([cls() for cls in pre_feature_generator_list])
        self.generators.append([cls() for cls in transformation_generator_list])
        self.generators.append([cls() for cls in pre_enocode_feature_generator_list])
        self.generators.append([cls() for cls in local_encode_generator_list])
        self.generators.append([cls() for cls in global_dict_index_generator_list])
        self.generators.append([cls() for cls in post_feature_generator_list])
        self.generators.append([cls(final = True) for cls in final_generator_list])

        self.fit_analyze()

    def fit_analyze(self, *args, **kwargs): 
        child = list(self.pipeline.keys())[-1]
        max_id = child
        # sample data
        X = DataFrameAPI().instiate(self.dataset[self.main_table])
        sampled_data = X.may_sample()
        
        for generator in self.data_profiler:
            self.pipeline, child, max_id = generator.fit_prepare(self.pipeline, [child], max_id, sampled_data, self.y)
        print("Feature List generated, using analyzed feature tags to create data pipeline")
        ret = super().fit_analyze(*args, **kwargs)
        self.update_label()
        return ret