import math
import shapefile
import matplotlib.pyplot as plt
import numpy
from mpl_toolkits.mplot3d import Axes3D

filename = "test.pathline"
total_layers = 11
sub_plots_total = total_layers
sub_plots_col = 2
sub_plots_row = math.ceil(sub_plots_total / sub_plots_col)
# deep = [6,7,8,9,10,11]
# shallow = [1,2,3,4,5]
# fig3d = plt.figure(2)
select_layer = 11
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
    while pt_line != '':
        if pt_line.replace(' ', '').replace('\t', '').replace('\n', '') != '':
            fields = pt_line.split()
            id = int(fields[0])
            t = float(fields[3])
            x = float(fields[5])
            y = float(fields[6])
            z = float(fields[7])
            lay = int(fields[8])
            if id == id_old:
                xyzt.append([x, y, z, t])
            else:
                id_old = id  # The new particle
                sub_id = lay
                w.poly(parts = [xyzt])
                xyzt = []
                xyzt.append([x, y, z, t])
        pt_line = f.readline()
w.save("test_poly")


# Figure 3d
# sub_plot_id = str(sub_plots_row) + str(sub_plots_col)+str(sub_id)
# plt.figure(2).add_subplot(sub_plot_id, projection='3d')
# plt.figure(2)
# xp = numpy.asarray(xs)
# yp = numpy.asarray(ys)
# zp = numpy.asarray(zs)
# ax = fig3d.gca(projection='3d')
# ax.plot(xp, yp, zp)
# ax.plot([x], [y], [z], "bo")
# plt.title("3D plot")

# if lay == select_layer:
#     if ipt >0:  # Save previous pt1
#         pt0 = pt1
#     pt1 = [x, y, z, t]
#     if ipt > 0:
#         xyzt.append([pt0, pt1])
#     ipt += 1
#     print(str(ipt))
