import math
import shapefile
import matplotlib.pyplot as plt


class ModpathPlot:
    """Utility to create plots and shapefile for Modpath 6.0 from .pathline file,
         May be modified to used with older Modpath versions.
    """
    @staticmethod
    def pathline_to_polylines(filename, outshapefile, model_offset=[0.0, 0.0, 0.0]):
        """Create shapefile for pathlines
        Args:
            filename (str): input .pathline file name
            outshapefile (str): output shapefile name
            model_offset (list, float): [x_offset, y_offset, rotation angle]
        """
        # Set up shapefile writer and create empty fields
        w = shapefile.Writer(shapefile.POLYLINE)
        w.field("ID_N")
        w.field("LAY_N")
        offset_x = model_offset[0]
        offset_y = model_offset[1]
        rotation = model_offset[2]/360.0 * 2.0 * math.pi
        # Start processing data
        xs = []
        ys = []
        zs = []
        pt = []
        id_old = 0  # do not have particle 0
        lay_old = 0 # do not have layer 0
        with open(filename, "r") as f:
            # Skip first three header lines
            for i in range(3):
                line_skip = f.readline()
            # Read the next line
            pt_line = f.readline()
            while pt_line != '':  # Keep reading until the end
                if pt_line.replace(' ', '').replace('\t', '').replace('\n', '') != '':
                    fields = pt_line.split()
                    id = int(fields[0])
                    t = float(fields[4])
                    x_nonproj = float(fields[5])
                    y_nonproj = float(fields[6])
                    z = float(fields[7])
                    lay = int(fields[8])
                    r = math.sqrt((x_nonproj*x_nonproj + y_nonproj*y_nonproj))
                    theta = math.atan2(y_nonproj, x_nonproj) + rotation
                    x = r*math.cos(theta) + offset_x
                    y = r*math.sin(theta) + offset_y
                    if id == id_old:
                        if lay == lay_old:  # If the same id, append to xyzt
                            pt.append([x, y, z, lay])
                        else:
                            # w.poly(parts=[pt])  # Write the geometry, polylines
                            w.line(parts=[pt])
                            w.record(id_old, lay_old)   # write the attributes
                            pt = []
                            pt.append([x, y, z, lay])
                            id_old = id  # The new particle
                            lay_old = lay
                    else:  # if not, plot the previous list xyzt, start new list
                        if id_old != 0:  # Start from id_old = 1
                            # w.poly(parts=[pt])
                            w.line(parts = [pt])
                            w.record(id_old, lay_old)
                        pt = []
                        pt.append([x, y, z, lay])
                        id_old = id  # The new particle
                        lay_old = lay
                pt_line = f.readline()
        w.save(outshapefile)  # save shapefile


    @staticmethod
    def pathline_to_points(filename, outshapefile):
        """Create all points shapefile for pathlines"""
        # Set up shapefile writer and create empty fields
        w = shapefile.Writer(shapefile.POINT)
        w.field("X")
        w.field("Y")
        w.field("Z")
        w.field("T")
        # Start processing data
        xs = []
        ys = []
        zs = []
        pt = []
        id_old = 0  # do not have particle 0
        lay_old = 0 # do not have layer 0
        with open(filename, "r") as f:
            # Skip first three header lines
            for i in range(3):
                line_skip = f.readline()
            # Read the next line
            pt_line = f.readline()
            while pt_line != '':  # Keep reading until the end
                if pt_line.replace(' ', '').replace('\t', '').replace('\n', '') != '':
                    fields = pt_line.split()
                    id = int(fields[0])
                    t = float(fields[4])
                    x = float(fields[5])
                    y = float(fields[6])
                    z = float(fields[7])
                    lay = int(fields[8])
                    w.point(x, y, z, lay)
                    w.record(x, y, z, lay)
                pt_line = f.readline()
        w.save(outshapefile)  # save shapefile

    @staticmethod
    def pathline_to_2dplot(filename, total_layers):
        """Create jpg and png for 2d particle path plots,
        each subplot contains pathlines from different layer origines"""
        sub_plots_total = total_layers
        sub_plots_col = 2
        sub_plots_row = math.ceil(sub_plots_total / sub_plots_col)
        xs = []
        ys = []
        zs = []
        id_old = 1
        xmax = 0.0
        ymax = 0.0
        with open(filename, "r") as f:
            # Skip first three header lines
            for i in range(3):
                line_skip = f.readline()
            # Read the next line
            pt_line = f.readline()
            while pt_line != '':
                if pt_line.replace(' ', '').replace('\t', '').replace('\n', '') != '':
                    fields = pt_line.split()
                    id = int(fields[0])
                    # t = float(fields[3])
                    x = float(fields[5])
                    if x > xmax:
                        xmax = x
                    y = float(fields[6])
                    if y > ymax:
                        ymax = y
                    z = float(fields[7])
                    lay = int(fields[8])
                    if id == id_old:
                        xs.append(x)
                        ys.append(y)
                        zs.append(z)
                    else:
                        id_old = id  # The new particle
                        sub_id = lay
                        plt.subplot(sub_plots_row,sub_plots_col, sub_id)
                        plt.plot(xs, ys, "r")
                        plt.plot(x, y, "b.")
                        plt.title("Layer"+str(lay))
                        plt.xlim(0.0, 1.1*xmax)
                        plt.ylim(0.0, 1.1*ymax)
                        plt.grid(True)
                        xs = []
                        xs.append(x)
                        ys = []
                        ys.append(y)
                        zs = []
                        zs.append(z)
                pt_line = f.readline()
        plt.figure(1)
        fig = plt.gcf()
        fignm = 'pathlines2d.jpg'
        fig.savefig(fignm)
        fignm = 'pathlines2d.png'
        fig.savefig(fignm)

if __name__ == "__main__":
    # User provide file name and total number of layers:
    # filename = "test.pathline"
    filename = "Garvey_30yr_mf.pathline"
    total_layers = 11
    # Plot 2d plots
    ModpathPlot.pathline_to_2dplot(filename, total_layers)
    # Create shapefile
    offset_x = 2077435.90287249
    offset_y = 266470.723511388
    rotation = -9
    model_offset = [offset_x, offset_y, rotation]
    ModpathPlot.pathline_to_polylines(filename, "test_polyline.shp", model_offset)
    # Create shapefile
    # ModpathPlot.pathline_to_points(filename, "test_points.shp")