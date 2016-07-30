import math
import shapefile
import matplotlib.pyplot as plt


class ModpathPlot:
    """Utility to create plots and shapefile for Modpath 6.0 from .pathline file,
         May be modified to used with older Modpath versions.
    """
    @staticmethod
    def pathline_to_shape(filename, total_layers):
        """Create shapefile for pathlines"""
        # Subplot lay out, I use two columns to layout subplots
        sub_plots_total = total_layers
        sub_plots_col = 2
        sub_plots_row = math.ceil(sub_plots_total / sub_plots_col)
        # Start processing
        xs = []
        ys = []
        zs = []
        xyzt = []
        id_old = 1
        w = shapefile.Writer(shapefile.POLYLINE)
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
                    t = float(fields[3])
                    x = float(fields[5])
                    y = float(fields[6])
                    z = float(fields[7])
                    lay = int(fields[8])
                    if id == id_old:  # If the same id, append to xyzt
                        xyzt.append([x, y, z, t])
                    else:  # if not, plot the previous list xyzt, start new list
                        id_old = id  # The new particle
                        sub_id = lay
                        w.poly(parts = [xyzt])
                        xyzt = []
                        xyzt.append([x, y, z, t])
                pt_line = f.readline()
        w.save("test_poly")  # save shapefile

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
                        plt.xlim(0.0, xmax)
                        plt.ylim(0.0, ymax)
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
    filename = "test.pathline"
    total_layers = 11
    # Plot 2d plots
    ModpathPlot.pathline_to_2dplot(filename, total_layers)
    # Create shapefile
    ModpathPlot.pathline_to_shape(filename, total_layers)
