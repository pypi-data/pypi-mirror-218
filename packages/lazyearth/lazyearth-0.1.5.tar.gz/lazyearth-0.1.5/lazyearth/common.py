import subprocess
import numpy
try:
    import matplotlib.pyplot as plt
except:
    print("install matplolib ...")
    subprocess.run('pip install matplolib',shell='true')
    import matplotlib.pyplot as plt
from matplotlib import colors
try:
    import xarray
except:
    print("install xarray ...")
    subprocess.run('pip install xarray',shell='true')
    import xarray
try:
    import sklearn
except:
    print("install sklean ...")
    subprocess.run('pip install -U scikit-learn',shell='true')
    import sklearn
    
try:
    from osgeo import gdal
except:
    #TODO set env conda env ไม่รู้จัก path
    raise ModuleNotFoundError('1.You have to install gdal first with this command "conda install -c conda-forge gdal" 2.pip install lazyearth again')

import lazyearth.virtual as vt
import lazyearth.plot as p

class objearth():
    def __init__(self):
        pass  
    @staticmethod
    def genimg(size=(2,2),datarange=(-1,1),nan=0,inf=0):    # verify : Datacube /
        """
        genimg()
        ---------
        Generate a 2D image with random values and specified amounts of NaN and Infinity values.

        This function generates a 2D array of random values within a specified range, 
        simulating an image (e.g., satellite image) that may contain abnormal data like NaN or Infinity. 
        The number of NaN and Infinity values to be included can be specified.

        Parameters
        size : tuple of int, optional
            A tuple containing two elements that represent the size (height and width) of the generated image. 
            Default is (2, 2).
        datarange : tuple of float, optional
            The range of possible values for the random data in the image. Default is (-1, 1).
        nan : int, optional
            The number of NaN values to include in the image. Default is 0.
        inf : int, optional
            The number of Infinity values to include in the image. Default is 0.
        
        Examples
        --------
        Generate a 2D image with random values, of size 5x5, including 2 NaNs and 1 Infinity value:
        >>> g = genimg((5, 5), nan=2, inf=1)
        ----------

        Returns
        -------
        ndarray
            A 2D array of floats representing the generated image. It may include NaN and Infinity values.
        """
        data = numpy.random.uniform(datarange[0],datarange[1],[size[0],size[1]])
        index_nan = numpy.random.choice(data.size,nan,replace=1)
        data.ravel()[index_nan] = numpy.nan
        index_inf = numpy.random.choice(data.size,inf,replace=1)
        data.ravel()[index_inf] = numpy.inf
        return data

    @staticmethod
    def gengaussian(size=(10,10)):   # verify : Datacube /
        """
        gengaussian()
        ---------
        Generate a 2D Gaussian function array.
        
        This function generates a 2D Gaussian array given the specified size. The Gaussian 
        function is centered around 1.0 ('mu') with a standard deviation of 0.5 ('sigma'). 
        The function creates a meshgrid based on the provided size and applies the Gaussian 
        function to it.
        
        Parameters
        ---------
        size : tuple of int, optional
            A tuple containing two elements that represent the size of the output array.
            The first element is the number of rows (height) and the second one is the number of columns (width). 
            Default is (10, 10).
        
        Examples
        ---------
        Generate a 2D Gaussian array of size 5x5:
        >>> g = gengaussian((5,5))

        Returns
        ---------
        ndarray
            A 2D array of floats representing the generated Gaussian function.
        """
        x, y = numpy.meshgrid(numpy.linspace(-1,1,size[0]), numpy.linspace(-1,1,size[1]))
        d = numpy.sqrt(x*x+y*y)
        sigma, mu = 0.5, 1.0
        g = numpy.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
        return g
    
    @staticmethod
    def bandopen(image_path):    # Verify : 
        """
        bandopen(image_path)
        ---------
        Open a satellite image (in TIFF format) and convert it to a NumPy array.

        This function provides an easy way to read a satellite image file and convert it into 
        a NumPy array, ready for further analysis.

        Parameters
        ---------
        image_path : str
            The file path to the satellite image in TIFF format.

        Examples
        ---------
        Open a blue band image of a Landsat 8 satellite:
        >>> blue = oe.bandopen(r"...\LC08_L1TP_130055_20160302_20170328_01_T1_sr_band2.tif")

        Returns
        -------
        ndarray
            The satellite image data as a 2D NumPy array.
        """
        return gdal.Open(image_path).ReadAsArray()

    @staticmethod
    def montage(img1,img2):    # verify : Datacube /
        """
        montage(img1,img2)
        ---------
        Compare two images by displaying them side by side.

        This function uses matplotlib to create a side-by-side comparison of two images 
        provided as numpy arrays. Each image is displayed in a subplot with a 'viridis' colormap.

        Parameters
        ----------
        img1 : numpy.ndarray
            The first image as a numpy array.
        img2 : numpy.ndarray
            The second image as a numpy array.

        Examples
        --------
        Compare Truecolor and Falsecolor images:
        >>> Tc = oe.truecolor(ds)
        >>> Fc = oe.Falsecolor(ds.red, ds.nir, ds.swir1)
        >>> oe.montage(Tc, Fc)
        
        Returns
        -------
        None
        """
        plt.figure(figsize=(15,15))
        plt.subplot(121),plt.imshow(img1, cmap = 'viridis')
        plt.title('Image 1'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img2, cmap = 'viridis')
        plt.title('Image 2'), plt.xticks([]), plt.yticks([])
        plt.show()
        plt.figure(figsize=(15,15))
        plt.subplot(121),plt.imshow(img1, cmap = 'gray')
        plt.title('Image 1'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img2, cmap = 'viridis')
        plt.title('Image 2'), plt.xticks([]), plt.yticks([])
        plt.show()

    @staticmethod
    def truecolor(Dataset, bright=10):    #verify
        """
        truecolor(Dataset)
        Generate a truecolor (RGB) image from an Xarray Dataset.

        This function takes an Xarray dataset containing satellite data, specifically red, green, and blue bands,
        and generates a corresponding truecolor image. Before creating the image, the function replaces 
        any values of -9999 (typically indicating missing data) with NaN, normalizes and multiplies with brightness factor.

        Parameters
        ----------
        Dataset : xarray.core.dataset.Dataset
            An Xarray Dataset containing red, green, and blue bands.
        bright : int, optional
            The brightness factor by which to multiply the normalized band values. Default is 10.

        Examples
        --------
        Create a truecolor image from a satellite data Xarray dataset:
        >>> Tc = oe.truecolor(ds)

        Returns
        -------
        ndarray
            A 3D ndarray representing the truecolor (RGB) image. The first two dimensions are the 
            spatial dimensions of the image, and the third dimension (size 3) represents the red, 
            green, and blue channels, respectively.
        """
        RED    = xarray.where(Dataset.red==-9999,numpy.nan,Dataset.red)
        red    = RED.to_numpy()/10000*bright
        BLUE   = xarray.where(Dataset.blue==-9999,numpy.nan,Dataset.blue)
        blue   = BLUE.to_numpy()/10000*bright
        GREEN  = xarray.where(Dataset.green==-9999,numpy.nan,Dataset.green)
        green  = GREEN.to_numpy()/10000*bright
        rgb    = numpy.stack([red,green,blue],axis=2)
        return rgb
    
    @staticmethod
    def falsecolor(Dataset1, Dataset2, Dataset3, bright=10):          
        """
        Generate a falsecolor image from three given Xarray DataArrays.

        This function creates a falsecolor image by combining three specified bands from satellite data. 
        Before combining, it replaces any -9999 values (typically indicating missing data) with NaN, 
        then normalizes the band values by dividing them by 10000, and finally multiplies by a specified brightness factor.

        Parameters
        ----------
        Dataset1 : xarray.core.dataarray.DataArray
            The first band to use in the false color image.
        Dataset2 : xarray.core.dataarray.DataArray
            The second band to use in the false color image.
        Dataset3 : xarray.core.dataarray.DataArray
            The third band to use in the false color image.
        bright : int, optional
            The brightness factor by which to multiply the normalized band values. Default is 10.

        Examples
        --------
        Generate a false color image using the NIR, red, and SWIR1 bands:
        >>> Fc = oe.falsecolor(ds.nir, ds.red, ds.swir1)

        Returns
        -------
        ndarray
            A 3D ndarray representing the false color image. The first two dimensions are the 
            spatial dimensions of the image, and the third dimension (size 3) represents the 
            three input bands, respectively.
        """
        BAND1    = xarray.where(Dataset1==-9999,numpy.nan,Dataset1)
        band1    = BAND1.to_numpy()/10000*bright
        BAND2    = xarray.where(Dataset2==-9999,numpy.nan,Dataset2)
        band2    = BAND2.to_numpy()/10000*bright
        BAND3    = xarray.where(Dataset3==-9999,numpy.nan,Dataset3)
        band3    = BAND3.to_numpy()/10000*bright
        product  = numpy.stack([band1,band2,band3],axis=2)
        return product


    
    # Fix bug
    # @staticmethod
    # def geo_save(array,filename,geo_transform = (0.0,1.0,0.0,0.0,0.0,1.0),projection='',dtype=gdal.GDT_Byte):
    #     """
    #     Save array to image
    #     :param array    : ndarray
    #     :param filename : filename
    #     :return         : TIFF image 
    #     """
    #     filename = Path(os.getcwd()).joinpath(filename+'.tif').as_posix()
    #     cols = array.shape[1]
    #     rows = array.shape[0]
    #     driver = gdal.GetDriverByName('GTiff')
    #     out_raster = driver.Create(filename,cols,rows,1,dtype,options=['COMPRESS=PACKBITS'])
    #     out_raster.SetGeoTransform(geo_transform)
    #     out_raster.SetProjection(projection)
    #     outband=out_raster.GetRasterBand(1)
    #     outband.SetNoDataValue(0)
    #     outband.WriteArray(array)
    #     outband.FlushCache()
    #     print('Saving image: '+filename)


    def bandcombination(band1, band2, band3, bright=10):       
        """
        Combination of any 3 bands from the same layer.
        This function creates a numpy 3D array by normalizing the input bands by 10000 and then scaling up by the 'bright' parameter.

        Parameters
        ----------
        band1 : numpy.ndarray
            The first band to combine. Expected shape is (M, N) where M and N are the dimensions of the image.
        band2 : numpy.ndarray
            The second band to combine. Expected shape is (M, N).
        band3 : numpy.ndarray
            The third band to combine. Expected shape is (M, N).
        bright : int, optional
            The brightness factor to scale the image by. Default is 10.

        Examples
        --------
        Generate color infrared with Near infrared, red and green bands
        >>> Ci = oe.bandcombination(nir, red, green)
        
        Returns
        -------
        numpy.ndarray
            A 3D array of floats (M, N, 3) representing the generated image. It may include NaN and Infinity values.
        """
        b1  = band1/10000 * bright
        b2  = band2/10000 * bright
        b3  = band3/10000 * bright
        return numpy.stack([b1, b2, b3], axis=2)


    @staticmethod
    def plotshow(*args,**kwargs):
        """
        Plot one or more images of various types and dimensions, with optional zoom.

        This function is capable of plotting various types of images, including numpy 2D/3D arrays and xarray DataArrays. 
        It can plot multiple images at once in a table-like format using plt.subplot(). 
        The function also provides several customization options through keyword arguments, including the ability to zoom into all images.

        Parameters
        ----------
        args : numpy.ndarray or xarray.core.dataarray.DataArray
            One or more images to plot. Each argument can be a numpy array (2D or 3D) or an xarray DataArray.

        kwargs : 
            area : list, optional
                A list of 4 elements [xmin, xmax, ymin, ymax] to zoom into all images. Default is None, which means no zoom.
            figsize : tuple, optional
                The size of the display. Default is (7,7).
            ts : float, optional
                The transparency of grid lines on the image. Default is 0.07.
            cmap : str or bool, optional
                The colormap to use. If True, uses the default colormap. Default is True.
            title : str, optional
                The title of the plot. Default is an empty string.
            xlabel : str, optional
                The label for the x-axis. Default is "x axis size".
            ylabel : str, optional
                The label for the y-axis. Default is "y axis size".

        Examples
        --------
        Plot a numpy array image:
        >>> oe.plotshow(img)

        Plot more than one image:
        >>> oe.plotshow(img1, img2, img3)

        Plot with custom properties and zoom:
        >>> oe.plotshow(img1, img2, img3, area=[200,300,0,100], figsize=(10,10), title='My Image', xlabel='Width', ylabel='Height')

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If an unsupported data type is provided.
        """
        # print(len(args))
        # 1 image mode
        if len(args)==1:
            DataArray = args[0]
            if 'figsize' in kwargs:
                    figsize = kwargs['figsize']
            else:
                figsize=(7,7)
            if 'title' in kwargs:
                title = kwargs['title']
            else:
                title = ""
            if 'xlabel' in kwargs:
                xlabel = kwargs['xlabel']
            else:
                xlabel = "x axis size"
            if 'ylabel' in kwargs:
                ylabel = kwargs['ylabel']
            else:
                ylabel = "y axis size"
            if 'ts' in kwargs:
                ts = kwargs['ts']
            else:
                ts = 0.07
            if 'cmap' in kwargs:
                cmap = kwargs['cmap']
            else:
                cmap = True

            # 01 xarray Data
            if type(DataArray) == xarray.core.dataarray.DataArray:
                # print("This is xarray")
                if 'area' in kwargs:
                    ymax = kwargs['area'][0]
                    ymin = kwargs['area'][1]
                    xmin = kwargs['area'][2]
                    xmax = kwargs['area'][3]
                else:
                    ymax = 0
                    ymin = args[0].shape[0]
                    xmin = 0
                    xmax = args[0].shape[1]
                lon  =  DataArray.longitude.to_numpy()[xmin:xmax]
                lon0 =  lon[0] ; lon1 =  lon[-1]
                lat  =  DataArray.latitude.to_numpy()[ymax:ymin]
                lat0 = -lat[-1] ; lat1 = -lat[0]
                def longitude(lon):
                    return [lon0,lon1]
                def latitude(lat):
                    return [lat0,lat1]
                def axis(x=0):
                    return x
                fig,ax = plt.subplots(constrained_layout=True)
                fig.set_size_inches(figsize)
                ax.set_title(title)
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.imshow(DataArray[ymax:ymin,xmin:xmax],extent=[xmin,xmax,ymin,ymax])
                secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
                secax_x.set_xlabel('longitude')
                secax_x = ax.secondary_xaxis('top',functions=(longitude,axis))
                secax_x.set_xlabel('longitude')
                secax_y = ax.secondary_yaxis('right',functions=(latitude,axis))
                secax_y.set_ylabel('latitute')
                plt.grid(color='w', linestyle='-', linewidth=ts)
                plt.show()
            # 02 Numpy Data
            elif type(DataArray) == numpy.ndarray:
                if 'area' in kwargs:
                    ymax = kwargs['area'][0]
                    ymin = kwargs['area'][1]
                    xmin = kwargs['area'][2]
                    xmax = kwargs['area'][3]
                else:
                    ymax = 0
                    ymin = args[0].shape[0]
                    xmin = 0
                    xmax = args[0].shape[1]
                # print("This is numpy")
                real_margin_img = DataArray[ymax:ymin,xmin:xmax]

                #plotshow
                plt.figure(figsize=(figsize))
                plt.subplots(constrained_layout=True)
                color_map = plt.imshow(real_margin_img,extent=[xmin,xmax,ymin,ymax])

                plt.title(title)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                plt.grid(color='w', linestyle='-', linewidth=ts)
                # faction
                im_ratio = real_margin_img.shape[1]/real_margin_img.shape[0]
                if im_ratio<1:
                    fac = 0.0485
                elif im_ratio==1:
                    fac = 0.045
                else:
                    fac = 0.0456*(im_ratio**(-1.0113))
                # print(real_margin_img.shape[1],real_margin_img.shape[0],im_ratio,fac)

                #colorbar
                min = real_margin_img.min()
                max = real_margin_img.max()
                plt.clim(min,max)
                if cmap==True:
                    color_map.set_cmap('viridis')
                else:
                    color_map.set_cmap(cmap)
                plt.colorbar(orientation="vertical",fraction=fac)
                plt.show()
            # 03 waterquality
            # print(len(args[0]))
            elif type(args[0]) == dict and len(args[0]) == 3:
                if 'area' in kwargs:
                    ymax = kwargs['area'][0]
                    ymin = kwargs['area'][1]
                    xmin = kwargs['area'][2]
                    xmax = kwargs['area'][3]
                else:
                    ymax = 0
                    ymin = args[0]['DataArray'].shape[0]
                    xmin = 0
                    xmax = args[0]['DataArray'].shape[1]
                DataArray = args[0]['DataArray']
                min_value = args[0]['Datavalue'][0]
                max_value = args[0]['Datavalue'][1]
                colormap  = args[0]['Datacolor']
                # colormap='jet'
                real_margin_img = DataArray[ymax:ymin,xmin:xmax]
                #plotshow
                plt.figure(figsize=(figsize))
                plt.subplots(constrained_layout=True)
                color_map = plt.imshow(real_margin_img,extent=[xmin,xmax,ymin,ymax])
                # faction
                im_ratio = real_margin_img.shape[1]/real_margin_img.shape[0]
                if im_ratio<1:
                    fac = 0.0485
                elif im_ratio==1:
                    fac = 0.045
                else:
                    fac = 0.0456*(im_ratio**(-1.0113))
                    # print(real_margin_img.shape[1],real_margin_img.shape[0],im_ratio,fac)
                #colorbar
                plt.clim(min_value,max_value)
                # color_map.set_cmap('viridis')
                if colormap != None:
                        cmap = plt.get_cmap(colormap)
                else:
                        cmap = vt.bluesea()
                color_map.set_cmap(cmap)
                plt.colorbar(orientation="vertical",fraction=fac,label='Pollution\nmg/l')
                # plt.set_label('x')
                plt.show()

            # Error
            else:
                raise ValueError("Nonetype :",type(DataArray))
        # more that 1 image mode 
        else:
            #clean waterquality type
            Ags = []
            for i in range(len(args)):
                if type(args[i])==dict:
                    Ags.append(args[i]['DataArray'])
                else:
                    Ags.append(args[i])
            args = Ags
            if 'area' in kwargs:
                ymax = kwargs['area'][0]
                ymin = kwargs['area'][1]
                xmin = kwargs['area'][2]
                xmax = kwargs['area'][3]
            else:
                ymax = 0
                ymin = args[0].shape[0]
                xmin = 0
                xmax = args[0].shape[1]
            Dl = len(args)
            img = args
            if Dl==2:
                p.plot02(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                )
            elif Dl==3:
                p.plot03(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                )
            elif Dl==4:
                p.plot04(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                )
            elif Dl==5:
                p.plot05(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                )
            elif Dl==6:
                p.plot06(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                )
            elif Dl==7:
                p.plot07(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                ,img[6][ymax:ymin,xmin:xmax]
                )
            elif Dl==8:
                p.plot08(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                ,img[6][ymax:ymin,xmin:xmax]
                ,img[7][ymax:ymin,xmin:xmax]
                )
            elif Dl==9:
                p.plot09(img[0][ymax:ymin,xmin:xmax]
                ,img[1][ymax:ymin,xmin:xmax]
                ,img[2][ymax:ymin,xmin:xmax]
                ,img[3][ymax:ymin,xmin:xmax]
                ,img[4][ymax:ymin,xmin:xmax]
                ,img[5][ymax:ymin,xmin:xmax]
                ,img[6][ymax:ymin,xmin:xmax]
                ,img[7][ymax:ymin,xmin:xmax]
                ,img[8][ymax:ymin,xmin:xmax]
                )
            else:
                print('error')

    @staticmethod 
    def stamp(project=''):             #verify
        import datetime,platform
        print(datetime.datetime.now().strftime('"""\n%c'))
        print('name :',project)
        print('OS system : ',platform.system())
        print('@author : Tun.k\n"""')
    # stamp()
