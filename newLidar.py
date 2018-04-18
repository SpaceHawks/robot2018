from hokuyolx import HokuyoLX
laser = HokuyoLX()
timestamp, scan = laser.get_filtered_intens() # Single measurment mode
print(scan.transpose())
# Continous measurment mode
# for timestamp, scan in laser.iter_dist(10):
#     print(timestamp)