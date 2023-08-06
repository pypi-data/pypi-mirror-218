import numpy as np
import pandas as pd


class Filter_for_data():

    # Lambda functions for filter window sum
    avg_summary = (lambda self, arr, i, x: np.sum(arr[i-x:i+x]))
    bg_summary = (lambda self, arr, i, x: np.sum(arr[0:i+x]))
    nd_summary = (lambda self, arr, i, x: np.sum(arr[i-x:]))

    def __init__(self, x=5) -> None:

        self.winow_size = x

        return None

    def changing_for_nparr(self, df: np.ndarray) -> np.ndarray:
        ln = len(df)
        df_copy = np.copy(df)
        # Rewrite on numpy
        for i in range(ln):
            sumer = 0
            if ((i > self.winow_size) and
                    (i < (ln - self.winow_size - 1))):
                # Here I need to write lamda function to get summary of neibors
                sumer = self.avg_summary(df, i, self.winow_size)/(
                    self.winow_size + self.winow_size
                    )
            elif (i <= self.winow_size):
                sumer = self.bg_summary(
                    df, i, self.winow_size
                    )/(i + self.winow_size)
            else:
                sumer = self.nd_summary(
                    df, i, self.winow_size
                    )/(self.winow_size + ln - i)
            df_copy[i] = sumer
        return df_copy

    def with_np_arr(self, df: np.ndarray) -> np.ndarray:
        df = np.convolve(
            df,
            np.ones(self.winow_size, dtype=int),
            'valid')
        return df


class Analyse_For_Res():

    def __init__(self, x: float = 1) -> None:
        # Maybe here I will use hparam
        self.mid_mlt = x
        return None

    def get_result(self, arr: np.ndarray, point: int, median: float):

        self.narr = arr
        self.peak = point
        self.median = median * self.mid_mlt

        x = self.__find_bg_from_p__()
        y = self.__find_nd_from_p__()

        return x, y

    def __find_bg_from_p__(self) -> int:

        result = self.peak

        while (True):
            result -= 1
            if ((self.narr[result] <= self.median) or (result == 0)):
                break
        return result

    def __find_nd_from_p__(self) -> int:
        result = self.peak
        while (True):
            result += 1
            if ((self.narr[result] <= self.median) or
                    (result == len(self.narr) - 1)):
                break
        return result


class Method_for_nd_bg():

    def __init__(self) -> None:
        self.arrnm = np.array([])
        return None

    def cord_and_arr_info(self, arr, peaks, bgns, ends) -> None:
        # There are three arrayes
        self.date_arr = arr
        self.len = len(peaks)
        self.point_nd = ends
        self.bgn_point = bgns
        return None

    def get_result(self):
        self.__creation_for_mx_arr__()
        temp = np.partition(-self.arrnm, 100)
        result_args = np.median(temp[:100]) * -1
        self.arrnm = np.array([])

        return result_args

    def __creation_for_mx_arr__(self):
        for point in range(1, self.len):
            strt = self.point_nd[point-1]
            fnsh = self.bgn_point[point]
            stepr = (fnsh - strt)/3
            self.arrnm = np.append(
                self.arrnm,
                self.date_arr[np.int(strt + stepr):np.int(fnsh - stepr)]
                )
        return None


class Find_With_Line():

    def update(self, main_arr: np.ndarray, new_md: np.float32) -> None:

        self.array_with_vals = main_arr

        self.bgn_numpy = np.array([])
        self.end_numpy = np.array([])

        self.control_val = new_md
        # I would like to use another algorithm to find md
        # mn[5] + (mx[5] - mn[5]) * 0,2
        #                             \- 0,2 will be hiper parametr
        self.general_arr = np.array([])
        return None

    def __cicle__(self) -> np.ndarray:
        # I need to define vars here.
        # Maybe I will crete a struct for the bgn, end and peak
        array_of_points = np.array([], dtype=int)
        i = 0

        local_m = -1
        len_of_ip = 0
        array_of_local_point = np.array([], dtype=int)

        while (i < len(self.array_with_vals)):
            if (self.array_with_vals[i] >= self.control_val):
                len_of_ip += 1
                array_of_local_point = np.append(array_of_local_point, i)
                if (self.array_with_vals[i] > local_m):
                    local_m = self.array_with_vals[i]
            elif (len_of_ip > 0):
                len_of_ip = 0
                if (local_m > 2.4080):
                    array_of_points = np.append(
                        array_of_points, array_of_local_point
                        )
                local_m = -1
                array_of_local_point = np.array([])
            i += 1
        return array_of_points

    def get_results(self) -> np.ndarray:
        result = np.array(self.__cicle__(), dtype=np.int32)
        return result


class Speed_of_Buble():

    def __init__(self) -> None:
        # Maybe it's better to create table from pandas
        self.table = pd.DataFrame([])
        self.ln_btw = (2.5/2) * (10 ** (-4))
        # I need to peek correct time in my programm( sec or msec)
        self.column_num = 0
        return None
    # Here I would like to add peaks from one of channels

    def read_for_arr(self, new_column):
        self.table.insert(
            self.column_num, f'col_{self.column_num}', pd.Series(new_column),
            True
            )
        self.column_num += 1

        return True

    def find_speed_betwen_points(self) -> np.ndarray:

        # if len(channel_1) = len(chebbel_2) -> That's ok
        # else -> find way to check peaks nearby and skeep others
        array_of_time_btw_signal = np.ndarray([])
        point_chnl1 = 0
        point_chnl2 = 0
        len_cl, wt = self.table.shape
        while (True):
            if ((point_chnl1 >= len_cl) or (point_chnl2 >= len_cl)):
                break
            var_col0 = self.table['col_0'].iloc[point_chnl1]
            var_col1 = self.table['col_1'].iloc[point_chnl2]
            if (var_col0 < var_col1):
                array_of_time_btw_signal = np.append(
                    array_of_time_btw_signal, self.ln_btw/(var_col1 - var_col0)
                    )
                point_chnl1 += 1
                point_chnl2 += 1
            else:
                point_chnl2 += 1
        return array_of_time_btw_signal
