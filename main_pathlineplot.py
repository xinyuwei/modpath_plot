import math
import shapefile
import matplotlib.pyplot as plt
# import numpy
# from mpl_toolkits.mplot3d import Axes3D
header = "item1_Particle_ID, " \
         "item2_Particle_Group, " \
         "item3_Time Point Index, " \
         "item4_Cumulative_Time_Step, " \
         "item5_Tracking_Time, " \
         "item6_Global_X, " \
         "item7_Global_Y, " \
         "item8_Global_Z, " \
         "item9_Layer, " \
         "item10_Row, " \
         "item11_Column, " \
         "item12_Grid, " \
         "item13_Local_X, " \
         "item14_Local_Y, " \
         "item15_Local_Z, " \
         "item16_Line_Segment_Index"

# filename = input()
# if len(filename) == 0:
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
id_old = 1
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
            y = float(fields[6])
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
                plt.xlim(0.0, 34000.0)
                plt.ylim(0.0, 11000.0)
                plt.grid(True)
                xs = []
                xs.append(x)
                ys = []
                ys.append(y)
                zs = []
                zs.append(z)
                # if lay in shallow:
                #     sub_id = 1
                # else:
                #     sub_id = 2
        pt_line = f.readline()
plt.figure(1)
fig = plt.gcf()
fignm = 'pathlines2d.jpg'
fig.savefig(fignm)
fignm = 'pathlines2d.png'
fig.savefig(fignm)

# plt.figure(2)
# plt.xlim(0.0, 34000.0)
# plt.ylim(0.0, 11000.0)
# plt.grid(True)
# fig = plt.gcf()
# fignm = 'pathlines3d.jpg'
# fig.savefig(fignm)
# fignm = 'pathlines3d.png'
# fig.savefig(fignm)
# plt.show()
#
# w = shapefile.Writer(shapefile.POLYLINE)
# w.poly(parts = xyzt)
# w.save("test_poly")


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
