import numpy as np
import os 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import LineCollection


from matplotlib_dhi import *
from matplotlib_dhi import subplots
def import_multiple_pd0(paths,labels):
    '''
    reads multiple Workhorse ADCP files from a list of filepaths


    Parameters
    ----------
    paths : list
        list containing paths to each .pd0 file
    labels : TYPE
        DESCRIPTION.

    Returns
    -------
    ADCP_data : dict
        Dictionary with keys specified by labels.

    '''
    ADCP_data = {}
    for p,path in enumerate(paths):
        label = labels[p]
        #path = row['Relative Data Location'].strip('\n').strip() # path to the ADCP data, strip formatting characters and spaces
        
        try:
            ADCP_data[label] = WorkhorseADCP.WorkhorseADCP(path)
        except: 
            print(f'Cound not read {path}')        
    return ADCP_data


#%% plot echo intensites
def echo_intensity_plot(adcp_file,**kwargs):#plot_by = 'bin',start_bin = None,end_bin = None,start_ensemble = None,end_ensemble = None,title = None):
    """
    Generate a fencegate plot of echo intensities 

    Parameters
    ----------
    adcp_file : object
        WorkhorseADCP object.
    plot_by : str
        y-axes plot method ('bin','depth').
    start_bin : int
        First bin to plot. (use zero based index)
    end_bin : int
        Last bin to plot.(use zero based index)
    start_ensemble : int
        First ensemble to plot.(use zero based index)
    end_ensemble : int
        Last ensemble to plot.(use zero based index)
    title : str
        plot axes title.

    Returns
    -------
    fig,ax
        matplotlib figure and axes objects

    """


    if kwargs.get('plot_by'):plot_by = kwargs.get('plot_by')
    else: plot_by = 'bin'
    
    if kwargs.get('start_bin'): start_bin = kwargs.get('start_bin')
    else: start_bin = 0
    
    if kwargs.get('end_bin'): end_bin = kwargs.get('end_bin')
    else: end_bin = adcp_file.n_bins
    

    if kwargs.get('start_ensemble'): start_ensemble = kwargs.get('start_ensemble')
    else: start_ensemble = 0
    
    if kwargs.get('end_ensemble'): end_ensemble = kwargs.get('end_ensemble')
    else: end_ensemble = adcp_file.n_ensembles   
    
    if kwargs.get('title'): title = kwargs.get('title')
    else: title = adcp_file.filepath.split(os.sep)[-1]
    
    
    nbins = (end_bin - start_bin)
    echo_intensity = adcp_file.get_ensemble_array(beam_number = 0, field_name = 'ECHO INTENSITY')[start_bin:end_bin,start_ensemble:end_ensemble]
    #echo_intensity = adcp_file.get_ensemble_array(beam_number = 0, field_name = 'CORRELATION MAGNITUDE')[start_bin:end_bin,start_ensemble:end_ensemble]
    ensemble_times = adcp_file.get_ensemble_datetimes()[start_ensemble:end_ensemble]
    

    subplot_titles = []
    fig,ax = subplots(nrow = 1, ncol = 2, figheight = 4, figwidth = 16, width_ratios = [4,1])
    

    ## format the ADCP data axes (left)
    topax = ax[0].twiny()
    ax[0].set_title(title)
    
    
    # set plot params based on instrument configuration 

    
    
    # set plotting extents in vertical direction
    if plot_by == 'bin':
        ylims = [start_bin,end_bin]
        ax[0].set_ylabel('Bin')
    elif plot_by == 'depth':
        bin_depths = adcp_file.get_bin_midpoints_depth()
        ylims = [bin_depths[start_bin],bin_depths[end_bin]]
        ax[0].set_ylabel('Depth')
    elif plot_by == 'HAB':
        bin_heights = adcp_file.get_bin_midpoints_HAB()
        ylims = [bin_heights[start_bin],bin_heights[end_bin]]
        ax[0].set_ylabel('Height Above Bed')
    else: 
        print('Invalid plot_by parameter')
    
    
    # set plotting extents in horizontal direction
    xlims = mdates.date2num(ensemble_times) # list of elegible xlimits 
    if adcp_file.beam_facing == 'UP':
        extent = [xlims[0],xlims[-1],ylims[0],ylims[1]]
    else:
        echo_intensity = np.flipud(echo_intensity)
        extent = [xlims[0],xlims[-1],ylims[1],ylims[0]]
        
        
    cmap = plt.cm.Spectral_r
    im = ax[0].imshow(echo_intensity, origin = 'lower', extent = extent, cmap = cmap, aspect = 'auto')
    cbar = fig.colorbar(im, ax=ax[0],orientation="vertical",location = 'left',fraction=0.046)
    cbar.set_label('Echo Intensity', rotation=90,fontsize= 8)
    
    

    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M %d%b%y '))
    topax.set_xlim(start_ensemble,end_ensemble)
    ax[0].set_xlabel('Ensemble')
    ax[0].grid(alpha = 0.1)
    ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation = -30, ha = 'left')
    
    
    
    ## Add a table with metadata 
    
    row_labels = ['File',
                  'Instrument S/N',
                  'Beam Facing',
                  'Instrument Depth (m)',
                  'Instrument HAB (m)',
                  'Frequency',
                  'First\Last Ensemble',
                  'First Date',
                  'Last Date',
                  'Elapsed Time (hr)',
                  'Start Bin',
                  'End Bin',]
    
    try:
        beam_dir = adcp_file.beam_facing
        sysfreq  = adcp_file.ensemble_data[0]['SYSTEM CONFIGURATION']['FREQUENCY']
    except:
        beam_dir = 'unknown'
        sysfreq  = 'unknown'
    
    cell_text = [adcp_file.filepath.split(os.sep)[-1],
                 str(adcp_file.ensemble_data[0]['FIXED LEADER']['INSTRUMENT SERIAL NUMBER']),
                 str(beam_dir),
                 str(adcp_file.instrument_depth),
                 str(adcp_file.instrument_HAB),
                 str(sysfreq),
                 str(start_ensemble)+' - '+str(end_ensemble),
                 ensemble_times[0].strftime('%d-%b-%y %H:%M:%S'),
                 ensemble_times[-1].strftime('%d-%b-%y %H:%M:%S'),
                 str(round((ensemble_times[-1]- ensemble_times[0]).total_seconds()/60/60,2)),
                 str(start_bin),
                 str(end_bin),]
    
    
    
    def left_justify_list(x):
        # left jsutify a list of strings so that they all have the same length
        x = cell_text 
        max_len = max([len(i) for i in x])
        
        for i in range(len(x)):
            x[i] = x[i].ljust(max_len)
        return x
        
    
    cell_text = [[i] for i in left_justify_list(cell_text)]    
    # pad each string on the right to have length 
    
    
    table = ax[1].table(cellText = cell_text,
                        rowLabels = row_labels,
                        rowLoc = 'left',
                        cellLoc = 'left',
                        bbox = [0.35,0,.95,1],alpha = 0.4)
    
    table.set_fontsize(9)
            
    ax[1].axis('off')
    ax[1].grid(False)
    ax[1].set_title("File Metadata",pad = 15)
    
    return fig,ax


#%%
def progressive_vector_plot(adcp_file,**kwargs):
    """
    

    Generate a progressive vector plot from the WorkhorseADCP class object 

    Parameters
    ----------
    adcp_file : object
        WorkhorseADCP object.
    color_by : str
        Coloring method ('bin','velocity','month').
    start_bin : int
        First bin to plot. (use zero based index)
    end_bin : int
        Last bin to plot.(use zero based index)
    start_ensemble : int
        First ensemble to plot.(use zero based index)
    end_ensemble : int
        Last ensemble to plot.(use zero based index)
    title : str
        plot axes title.

    Returns
    -------
    fig,ax
        matplotlib figure and axes objects

    """
    


    if kwargs.get('color_by'):color_by = kwargs.get('color_by')
    else: color_by = 'bin'
    
    if kwargs.get('start_bin'): start_bin = kwargs.get('start_bin')
    else: start_bin = 0
    
    if kwargs.get('end_bin'): end_bin = kwargs.get('end_bin')
    else: end_bin = adcp_file.n_bins-1
    
    if kwargs.get('start_ensemble'): start_ensemble = kwargs.get('start_ensemble')
    else: start_ensemble = 0
    
    if kwargs.get('end_ensemble'): end_ensemble= kwargs.get('end_ensemble')
    else: end_ensemble = adcp_file.n_ensembles   
    
    if kwargs.get('title'): title = kwargs.get('title')
    else: title = adcp_file.filepath.split(os.sep)[-1]     
    

    print(start_ensemble)
    
    #adcp_file = ADCP_data[ID]
    # start_ensemble = 0
    # end_ensemble = adcp_file.n_ensembles
    # start_bin = 0
    # end_bin = adcp_file.n_bins-1
    #color_by = 'bin' #velocity'  #bin'#'velocity'#'bin'
    
    
    plot = True
    nbins = (end_bin - start_bin)+1

    
    
    
    
    u,v,z,du,dv,dz,err = adcp_file.get_velocity()
    ensemble_times = adcp_file.get_ensemble_datetimes()[start_ensemble:end_ensemble]
    
    
    u = u[start_ensemble:end_ensemble,start_bin:end_bin+1]
    v = v[start_ensemble:end_ensemble,start_bin:end_bin+1]
    z = z[start_ensemble:end_ensemble,start_bin:end_bin+1]
    du = du[start_ensemble:end_ensemble,start_bin:end_bin+1]
    dv = dv[start_ensemble:end_ensemble,start_bin:end_bin+1]
    dz = dz[start_ensemble:end_ensemble,start_bin:end_bin+1]
    
    xy_speed = np.sqrt(u**2 + v**2)
    
    pu = np.nancumsum(du,axis = 0) #,-np.outer(du[0,:],np.ones(self.n_ensembles)).T])
    pv = np.nancumsum(dv,axis = 0) # ,-np.outer(dv[0,:],np.ones(self.n_ensembles)).T])
    pz = np.nancumsum(dz,axis = 0) # ,-np.outer(dz[0,:],np.ones(self.n_ensembles)).T])
    
    
    if plot:
        # fig = plt.figure()
        # ax = plt.gca()
        #fig, ax = plt.subplots(1, 2,gridspec_kw={'width_ratios': [3, 1]})
        
        fig,ax = DHI_subplots(nrow = 1, ncol = 2, figheight = 7, figwidth =9, width_ratios = [3,1])
 
        #ax[0].set_aspect('equal')
        ax[0].grid(alpha = 0.3)
        ax[0].set_xlabel('East Distance (m)')
        ax[0].set_ylabel('North Distance (m)')
        ax[0].set_title(title)
        #ax[0].set_aspect('equal',adjustable = 'datalim')
        

        cbar_shrink = .043#.75
        global points,segments
        
        if color_by == 'bin':

            cmap = plt.cm.Spectral  # define the colormap
            # extract all colors from the .jet map
            cmaplist = [cmap(i) for i in range(cmap.N)]
            # force the first color entry to be grey
            cmaplist[0] = (.5, .5, .5, 1.0)
            
            # create the new map
            cmap = mpl.colors.LinearSegmentedColormap.from_list(
                'Custom cmap', cmaplist, cmap.N)
            
            # define the bins and normalize
            bounds = np.linspace(0, nbins, nbins+1)
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
            for b in range(nbins):
                #ax[0].plot(pu[:,b],pv[:,b], label = f'Bin {start_bin+b}')#, c = cmap(b), norm = norm)#,color = colors[s],alpha = 0.6)
    
                points = np.array((pu[:-1,b], pv[:-1,b])).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                #norm = plt.Normalize(0, adcp_file.n_bins,1)
                lines = LineCollection(segments, cmap=cmap, norm=norm)
                lines.set_array(len(points)*[b])
                lines.set_linewidth(1)
                line = ax[0].add_collection(lines)           
            cbar = fig.colorbar(line, ax=ax[0],orientation="horizontal", pad=.2, fraction=cbar_shrink)
            cbar.set_label('Bin Number', rotation=0)
    
    
        elif color_by == 'velocity':
            cmap = plt.cm.jet
            for b in range(nbins):
                points = np.array((pu[:-1,b], pv[1:,b])).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                norm = plt.Normalize(0, np.quantile(xy_speed[~np.isnan(xy_speed)],0.99))
                lines = LineCollection(segments, cmap=cmap, norm=norm)
                lines.set_array(xy_speed[:,b])
                lines.set_linewidth(1)
                line = ax[0].add_collection(lines)
                #break
            cbar = fig.colorbar(line, ax=ax[0],orientation="horizontal", pad=.2, fraction = cbar_shrink)
            cbar.set_label('Velocity (m/s) ', rotation=0)
            
        elif color_by == 'month':
            cmap = plt.cm.get_cmap('tab20b', 12)
            def gen_interval(x):
                x = x.isoweekday()
                return x
            vgen_interval = np.vectorize(gen_interval)
            months = [i.month for i in ensemble_times]
            for b in range(nbins):
                points = np.array((pu[:-1,b], pv[1:,b])).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                norm = plt.Normalize(1,12)
                lines = LineCollection(segments, cmap=cmap, norm=norm)
                lines.set_array(months)
                lines.set_linewidth(1)
                line = ax[0].add_collection(lines)
                #break
            cbar = fig.colorbar(line, ax=ax[0],orientation="horizontal", pad=.2, fraction = cbar_shrink)
            cbar.set_label('Month of Year', rotation=0)        
            
            
        else:
            print(r'Invalid plot mode {color_by}')
    
        #set axes limits 
        xrange = 1.1*(np.nanmax(abs(pu)))
        yrange = 1.1*(np.nanmax(abs(pv)))
        
        rng = max(xrange,yrange)
        #print([np.nanmax(pu),xrange])
        # ax.set_xbound([-xrange,xrange])
        # ax.set_ybound([-yrange,yrange])
        
        ax[0].set_xlim(-rng,rng)
        ax[0].set_ylim(-rng,rng)
    
        ax[0].set_aspect('equal')
        ## Add a table with metadata 
        
        row_labels = ['File',
                      'Instrument S/N',
                      'Beam Facing',
                      'Frequency',
                      'First\Last Ensemble',
                      'First Date',
                      'Last Date',
                      'Elapsed Time (hr)',
                      'Start Bin',
                      'End Bin',
                      'Mean Speed (m/s)',
                      'StD Speed (m/s)',]
        try:
            beam_dir = adcp_file.beam_facing
            sysfreq  = adcp_file.ensemble_data[0]['SYSTEM CONFIGURATION']['FREQUENCY']
        except:
            beam_dir = 'unknown'
            sysfreq  = 'unknown'
               
        cell_text = [adcp_file.filepath.split(os.sep)[-1],
                     str(adcp_file.ensemble_data[0]['FIXED LEADER']['INSTRUMENT SERIAL NUMBER']),
                     beam_dir,
                     sysfreq,
                     str(start_ensemble)+' - '+str(end_ensemble),
                     ensemble_times[0].strftime('%d-%b-%y %H:%M:%S'),
                     ensemble_times[-1].strftime('%d-%b-%y %H:%M:%S'),
                     str((ensemble_times[-1]- ensemble_times[0]).total_seconds()/60/60),
                     str(start_bin),
                     str(end_bin),
                     str(round(np.nanmean(xy_speed),1)),
                     str(round(np.nanstd(xy_speed),1))]
        
        
        
        def left_justify_list(x):
            # left jsutify a list of strings so that they all have the same length
            x = cell_text 
            max_len = max([len(i) for i in x])
            
            for i in range(len(x)):
                x[i] = x[i].ljust(max_len)
            return x
            
        
        cell_text = [[i] for i in left_justify_list(cell_text)]    
        # pad each string on the right to have length 
        
        
        table = ax[1].table(cellText = cell_text,
                            rowLabels = row_labels,
                            rowLoc = 'left',
                            cellLoc = 'left',
                            bbox = [0.4,0.5,1,.5],alpha = 0.4)
        
        table.set_fontsize(9)
                
        ax[1].axis('off')
        ax[1].grid(False)
        ax[1].set_title("File Metadata")
        
    # progressive_vector_plot(ADCP_data[ID],
    #                         color_by = 'velocity',
    #                         start_bin = start_bin,
    #                         end_bin = end_bin,
    #                         start_ensemble = start_ensemble,
    #                         end_ensemble = end_ensemble)
    return fig,ax
#%%






