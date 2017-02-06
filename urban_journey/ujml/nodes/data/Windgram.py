import sys

import numpy as np
from scipy.interpolate import interp1d
import re
from datetime import datetime
from time import strptime

from urban_journey.common.cached import cached
from urban_journey.ujml.attributes import String, DateTime, FilePath
from urban_journey.ujml.data_node_base import DataNodeBase
from urban_journey.ujml.exceptions import RequiredAttributeError, DataLoadError
from sim_common.conversions import knot_to_m


class windgram(DataNodeBase):
    """
    Bases: :class:`urban_journey.DataNodeBase`

    Loads pressure data form a text file.
    return np.array with [p(Pa), heading(deg), speed(m/s)]
    """

    file = FilePath()
    hour = DateTime()
    int_type = String(optional_value='linear')
    encoding = String(optional_value='utf-8')

    @cached
    def data(self):
        heading = []  # for storing heading data
        speed = []  # for storing speed data
        p = []  # for storing pressure

        try:
            with open(self.file, 'r', encoding=self.encoding) as data_f:
                raw_windgram_data = data_f.readlines()

            # Legend of Windgram.txt
            # Line 0: name of file
            # Line 1: Latitude, Longitude
            # Line 2: Initial Time
            # Line 3: Initial Time of Calculations : dd mmm yyyy hh
            # Line 4: Duration of Calculations
            # Line 6: Information of data format and units
            # Line 7: Time of the Measurements
            # Line 9-EOF: Data

            t = re.findall(r'\d+\w+\d+', raw_windgram_data[3].replace(' ', ''))[0]
            time_calc = datetime(int(t[5:9]), strptime(t[2:5], '%b').tm_mon, int(t[0:2]), int(t[9:]))
            time_diff = (self.hour - time_calc).total_seconds()/3600


            num_h = raw_windgram_data[7].count('.')  # amount of time increments
            col_time = re.match(r"FHR:" + r"([+-]\d*[.])" * num_h, raw_windgram_data[7].replace(' ', ''))  # time value for each col measurement

            x = [float(i) for i in col_time.groups()]  # max_time = x[-1] ; min time = x[0]
            if time_diff > x[-1] or time_diff < x[0]:
                self.raise_exception(DataLoadError, "Windgram time over limit", extra_traceback=sys.exc_info()[2])
                #break?

            for i in range(9, len(raw_windgram_data)):
                data_col = re.match(r"\s*([\d\.]+)(?:mb)" + r"\s*(\d+)@(\d+)" * num_h, raw_windgram_data[i])
                heading.append([int(data_col.group(2 + 2 * j)) for j in range(num_h)])  # !
                speed.append([knot_to_m(int(data_col.group(3 + 2 * j))) for j in range(num_h)])  # convert from knot->m/s
                p.append(float(data_col.group(1))*100)  # convert from mb->Pa

            head_int = interp1d(x, heading, kind=self.int_type)
            speed_int = interp1d(x, speed, kind=self.int_type)
            head_res = head_int(time_diff)
            speed_res = speed_int(time_diff)

            return np.stack((p, speed_res, head_res), axis=-1)
        except RequiredAttributeError as e:
            raise e
        except:
            self.raise_exception(DataLoadError, "Windgram", extra_traceback=sys.exc_info()[2])

    def reset(self):
        del self.data
