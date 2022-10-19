import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd


class GECOLogConverter():
    """
    Convert CAEN GECO log file format to csv file

    Usage:
    gc = GECOLogConverter()
    gc.convert_to_csv('/path/to/your/geco/file.log')
    """

    def __init__(self) -> None:
        pass

    def convert_to_csv(self, file_name):
        self.filename=filename
        self.load_data()
        self.write()

    def ParseLine(self, line):
        words = line.split()
        ### example line for sy5527lc power supply:
        ### [2019-01-28T09:03:08]: [sy5527lc] bd [1] ch [4] par [VMon] val [23.78];
        ### [2019-01-28T09:03:15]: [sy5527lc] bd [1] ch [7] par [IMon] val [1.67485]; 
        timestamp_str = words[0].replace("[","").replace("]:","")
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
        board_id   = int(words[3].replace("[","").replace("]",""))
        ch_id       = int(words[5].replace("[","").replace("]",""))
        par_name     = words[7].replace("[","").replace("]","")
        value         = float(words[9].replace("[","").replace("];",""))
        return timestamp,board_id, ch_id,par_name,value

    def load_data(self):
        filename=self.filename
        data_dict = {
            'timestamp': [] , 
            'ch_id': [],
            'par_name':[], 
            'par_value':[]
        }
        with open(filename) as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]
            counter=0
            for line in lines:
                timestamp, board_id, ch_id, par_name, value = self.ParseLine(line)
                new_row={'timestamp': timestamp, 'ch_id': id, 'par_name': par_name, 'par_value': value}
                data_dict['timestamp'].append(timestamp)
                data_dict['ch_id'].append(board_id*100 + ch_id)
                data_dict['par_name'].append(par_name)
                data_dict['par_value'].append(value)
                counter += 1
            self.n_entries = counter
            self.df = pd.DataFrame(data_dict)

    def write(self):
        ofname = self.filename[:-4]+'.csv'
        self.df.to_csv(ofname, date_format='%Y-%m-%dT%H:%M:%S')


        
class GECOPlotter():
    """
    Get data as trend
    Produce plots
    """
    def __init__(self, file_list=[]) -> None:
        self.file_list = file_list
        self.merge_data()
        self.find_all_channels()

    def merge_data(self):
        file_list = self.file_list
        #mypaser = lambda x: pd.to_datetime.strptime(x, "%Y-%m-%dT%H:%M:%S")
        self.df = pd.DataFrame(columns=['timestamp', 'ch_id', 'par_name', 'par_value'])
        for f in file_list:
            df = pd.read_csv(f,  parse_dates=['timestamp'])
            self.df = self.df.append(df)

    def find_all_channels(self):
        df = self.df.head(1000)
        all_ch = pd.unique(df['ch_id'])
        self.all_ch = all_ch

    def get_imon_trend(self, ch_id):
        df = self.df
        mask = (df['par_name'] == 'IMon') & (df['ch_id'] == ch_id)
        t = df.loc[mask]['timestamp']
        y = df.loc[mask]['par_value']
        return t, y

    def plot_all_imon_trend(self, save_fig=False, fig_format='pdf'):
        """
        Args:
        save_fig: bool
        fig_format: str. options: pdf, png. If save_fig=False, this argument is ignored.
        """
        if save_fig:
            fig_name="IMon_all.%s" % fig_format
            
        ncols = 6
        nrows = 9
        plt.figure(figsize=[4*ncols,3*nrows], dpi=90)
        counter=0
        for i, k in enumerate(sorted(gp.all_ch)):
            ax = plt.subplot(nrows,ncols,counter+1)
            t, y = self.get_imon_trend(k)
            ym = np.mean(y)
            if ym<200:
                continue
            plt.plot(t, y, label='HV ch_id=%d' % k, marker='None')
            counter += 1
            plt.xticks(rotation=45, fontsize=9)
            plt.ylabel('IMon [uA]')
            #ymax = max( ym*1.002, max(y))
            #ymin = min( ym*0.998, min(y))
            #plt.ylim([ymin, ymax])
            plt.legend()
            plt.tight_layout()
        if save_fig:
            if len(gp.file_list)==1:
                fig_name = gp.file_list[0][:-4]+'.'+fig_format
            plt.savefig(fig_name)
        plt.show()
