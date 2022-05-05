#!/usr/bin/python3

import matplotlib.pyplot as plt

data = [[(3, 0.0, 'TRUE'), (5, 0.0, 'TRUE'), (7, 0.0, 'TRUE'), (9, 0.01, 'TRUE'), (11, 0.03, 'TRUE'), (13, 0.07, 'TRUE'), (15, 0.15, 'TRUE'), (17, 0.28, 'TRUE'), (19, 0.52, 'TRUE'), (21, 0.88, 'TRUE'), (23, 1.47, 'TRUE'), (25, 2.3, 'TRUE'), (27, 3.46, 'TRUE'), (29, 5.23, 'TRUE'), (31, 7.55, 'TRUE'), (33, 10.67, 'TRUE')], [(2, 0.0, 'FALSE'), (4, 0.0, 'FALSE'), (6, 0.0, 'FALSE'), (8, 0.01, 'FALSE'), (10, 0.02, 'FALSE'), (12, 0.05, 'FALSE'), (14, 0.1, 'FALSE'), (16, 0.21, 'FALSE'), (18, 0.39, 'FALSE'), (20, 0.68, 'FALSE'), (22, 1.13, 'FALSE'), (24, 1.83, 'FALSE'), (26, 2.83, 'FALSE'), (28, 4.23, 'FALSE'), (30, 6.31, 'FALSE'), (32, 9.03, 'FALSE'), (34, 12.64, 'FALSE')], [(10, 0.02, 'TRUE'), (12, 0.04, 'TRUE'), (14, 0.1, 'TRUE'), (16, 0.2, 'TRUE'), (18, 0.36, 'TRUE'), (20, 0.65, 'TRUE'), (22, 1.1, 'TRUE'), (24, 1.72, 'TRUE'), (26, 2.69, 'TRUE'), (28, 4.1, 'TRUE'), (30, 6.05, 'TRUE'), (32, 8.74, 'TRUE'), (34, 12.4, 'TRUE')], [(10, 0.02, 'FALSE'), (12, 0.04, 'FALSE'), (14, 0.1, 'FALSE'), (16, 0.2, 'FALSE'), (18, 0.36, 'FALSE'), (20, 0.65, 'FALSE'), (22, 1.1, 'FALSE'), (24, 1.74, 'FALSE'), (26, 2.69, 'FALSE'), (28, 4.15, 'FALSE'), (30, 6.04, 'FALSE'), (32, 8.77, 'FALSE'), (34, 12.39, 'FALSE')], [(10, 0.02, 'TRUE'), (12, 0.05, 'TRUE'), (14, 0.11, 'TRUE'), (16, 0.21, 'TRUE'), (18, 0.38, 'TRUE'), (20, 0.67, 'TRUE'), (22, 1.13, 'TRUE'), (24, 1.82, 'TRUE'), (26, 2.82, 'TRUE'), (28, 4.22, 'TRUE'), (30, 6.14, 'TRUE'), (32, 8.83, 'TRUE'), (34, 12.14, 'TRUE')], [(10, 0.02, 'FALSE'), (12, 0.05, 'FALSE'), (14, 0.11, 'FALSE'), (16, 0.21, 'FALSE'), (18, 0.38, 'FALSE'), (20, 0.68, 'FALSE'), (22, 1.13, 'FALSE'), (24, 1.78, 'FALSE'), (26, 2.74, 'FALSE'), (28, 4.21, 'FALSE'), (30, 6.2, 'FALSE'), (32, 8.89, 'FALSE'), (34, 12.21, 'FALSE')], [(10, 0.07, 'TRUE'), (12, 0.13, 'TRUE'), (14, 0.23, 'TRUE'), (16, 0.36, 'TRUE'), (18, 0.59, 'TRUE'), (20, 0.94, 'TRUE'), (22, 1.47, 'TRUE'), (24, 2.2, 'TRUE'), (26, 3.28, 'TRUE'), (28, 4.85, 'TRUE'), (30, 6.96, 'TRUE'), (32, 9.71, 'TRUE'), (34, 13.39, 'TRUE')], [(10, 0.07, 'FALSE'), (12, 0.12, 'FALSE'), (14, 0.22, 'FALSE'), (16, 0.35, 'FALSE'), (18, 0.59, 'FALSE'), (20, 0.92, 'FALSE'), (22, 1.46, 'FALSE'), (24, 2.21, 'FALSE'), (26, 3.28, 'FALSE'), (28, 4.81, 'FALSE'), (30, 6.95, 'FALSE'), (32, 9.75, 'FALSE'), (34, 13.41, 'FALSE')], [(10, 0.02, 'ERROR'), (12, 0.05, 'ERROR'), (14, 0.1, 'ERROR'), (16, 0.2, 'ERROR'), (18, 0.38, 'ERROR'), (20, 0.66, 'ERROR'), (22, 1.08, 'ERROR'), (24, 1.77, 'ERROR'), (26, 2.73, 'ERROR'), (28, 4.03, 'ERROR'), (30, 5.91, 'ERROR'), (32, 8.52, 'ERROR'), (34, 12.12, 'ERROR')], [(10, 0.02, 'FALSE'), (12, 0.05, 'FALSE'), (14, 0.1, 'FALSE'), (16, 0.21, 'FALSE'), (18, 0.37, 'FALSE'), (20, 0.65, 'FALSE'), (22, 1.09, 'FALSE'), (24, 1.79, 'FALSE'), (26, 2.69, 'FALSE'), (28, 4.1, 'FALSE'), (30, 6.03, 'FALSE'), (32, 8.72, 'FALSE'), (34, 12.04, 'FALSE')], [(10, 0.02, 'TRUE'), (12, 0.05, 'TRUE'), (14, 0.11, 'TRUE'), (16, 0.21, 'TRUE'), (18, 0.39, 'TRUE'), (20, 0.68, 'TRUE'), (22, 1.13, 'TRUE'), (24, 1.81, 'TRUE'), (26, 2.79, 'TRUE'), (28, 4.2, 'TRUE'), (30, 6.21, 'TRUE'), (32, 8.83, 'TRUE'), (34, 12.47, 'TRUE')], [(11, 0.03, 'FALSE'), (13, 0.07, 'FALSE'), (15, 0.15, 'FALSE'), (17, 0.28, 'FALSE'), (19, 0.51, 'FALSE'), (21, 0.87, 'FALSE'), (23, 1.43, 'FALSE'), (25, 2.24, 'FALSE'), (27, 3.43, 'FALSE'), (29, 5.09, 'FALSE'), (31, 7.38, 'FALSE'), (33, 10.48, 'FALSE')], [(11, 0.03, 'TRUE'), (13, 0.07, 'TRUE'), (15, 0.14, 'TRUE'), (17, 0.27, 'TRUE'), (19, 0.49, 'TRUE'), (21, 0.87, 'TRUE'), (23, 1.43, 'TRUE'), (25, 2.2, 'TRUE'), (27, 3.31, 'TRUE'), (29, 4.99, 'TRUE'), (31, 7.26, 'TRUE'), (33, 10.45, 'TRUE')], [(12, 0.04, 'FALSE'), (14, 0.1, 'FALSE'), (16, 0.2, 'FALSE'), (18, 0.36, 'FALSE'), (20, 0.65, 'FALSE'), (22, 1.09, 'FALSE'), (24, 1.77, 'FALSE'), (26, 2.68, 'FALSE'), (28, 4.06, 'FALSE'), (30, 6.02, 'FALSE'), (32, 8.75, 'FALSE'), (34, 12.4, 'FALSE')], [(10, 0.02, 'TRUE'), (12, 0.05, 'TRUE'), (14, 0.1, 'TRUE'), (16, 0.2, 'TRUE'), (18, 0.38, 'TRUE'), (20, 0.66, 'TRUE'), (22, 1.09, 'TRUE'), (24, 1.76, 'TRUE'), (26, 2.72, 'TRUE'), (28, 4.11, 'TRUE'), (30, 6.05, 'TRUE'), (32, 8.83, 'TRUE'), (34, 12.11, 'TRUE')], [(11, 0.04, 'FALSE'), (13, 0.07, 'FALSE'), (15, 0.19, 'FALSE'), (17, 0.29, 'FALSE'), (19, 0.5, 'FALSE'), (21, 0.85, 'FALSE'), (23, 1.4, 'FALSE'), (25, 2.2, 'FALSE'), (27, 3.48, 'FALSE'), (29, 4.97, 'FALSE'), (31, 7.41, 'FALSE'), (33, 10.22, 'FALSE')], [(12, 0.05, 'TRUE'), (14, 0.1, 'TRUE'), (16, 0.2, 'TRUE'), (18, 0.37, 'TRUE'), (20, 0.65, 'TRUE'), (22, 1.09, 'TRUE'), (24, 1.74, 'TRUE'), (26, 2.72, 'TRUE'), (28, 4.14, 'TRUE'), (30, 6.13, 'TRUE'), (32, 8.73, 'TRUE'), (34, 12.32, 'TRUE')], [(11, 0.03, 'FALSE'), (13, 0.07, 'FALSE'), (15, 0.14, 'FALSE'), (17, 0.27, 'FALSE'), (19, 0.5, 'FALSE'), (21, 0.85, 'FALSE'), (23, 1.4, 'FALSE'), (25, 2.2, 'FALSE'), (27, 3.4, 'FALSE'), (29, 5.07, 'FALSE'), (31, 7.32, 'FALSE'), (33, 10.33, 'FALSE')], [(11, 0.06, 'TRUE'), (13, 0.11, 'TRUE'), (15, 0.2, 'TRUE'), (17, 0.36, 'TRUE'), (19, 0.63, 'TRUE'), (21, 1.02, 'TRUE'), (23, 1.66, 'TRUE'), (25, 2.51, 'TRUE'), (27, 3.78, 'TRUE'), (29, 5.59, 'TRUE'), (31, 7.95, 'TRUE'), (33, 11.04, 'TRUE')], [(10, 0.04, 'FALSE'), (12, 0.07, 'FALSE'), (14, 0.15, 'FALSE'), (16, 0.27, 'FALSE'), (18, 0.47, 'FALSE'), (20, 0.78, 'FALSE'), (22, 1.28, 'FALSE'), (24, 2.01, 'FALSE'), (26, 3.04, 'FALSE'), (28, 4.52, 'FALSE'), (30, 6.63, 'FALSE'), (32, 9.33, 'FALSE'), (34, 12.91, 'FALSE')], [(11, 0.12, 'TRUE'), (13, 0.12, 'TRUE'), (15, 0.21, 'TRUE'), (17, 0.35, 'TRUE'), (19, 0.63, 'TRUE'), (21, 0.99, 'TRUE'), (23, 1.59, 'TRUE'), (25, 2.46, 'TRUE'), (27, 3.66, 'TRUE'), (29, 5.39, 'TRUE'), (31, 7.63, 'TRUE'), (33, 10.71, 'TRUE')], [(10, 0.05, 'FALSE'), (12, 0.08, 'FALSE'), (14, 0.15, 'FALSE'), (16, 0.27, 'FALSE'), (18, 0.47, 'FALSE'), (20, 0.79, 'FALSE'), (22, 1.25, 'FALSE'), (24, 1.99, 'FALSE'), (26, 2.99, 'FALSE'), (28, 4.48, 'FALSE'), (30, 6.44, 'FALSE'), (32, 9.07, 'FALSE'), (34, 12.7, 'FALSE')], [(8, 0.01, 'TRUE'), (12, 0.05, 'TRUE'), (12, 0.05, 'TRUE'), (16, 0.2, 'TRUE'), (16, 0.2, 'TRUE'), (20, 0.66, 'TRUE'), (20, 0.66, 'TRUE'), (24, 1.8, 'TRUE'), (24, 1.81, 'TRUE'), (28, 4.14, 'TRUE'), (28, 4.12, 'TRUE'), (32, 8.89, 'TRUE'), (32, 8.8, 'TRUE'), (36, 16.8, 'TRUE')], [(9, 0.01, 'FALSE'), (13, 0.07, 'FALSE'), (13, 0.07, 'FALSE'), (17, 0.28, 'FALSE'), (17, 0.28, 'FALSE'), (21, 0.85, 'FALSE'), (21, 0.85, 'FALSE'), (25, 2.25, 'FALSE'), (25, 2.24, 'FALSE'), (29, 5.04, 'FALSE'), (29, 5.02, 'FALSE'), (33, 10.49, 'FALSE')], [(9, 0.01, 'TRUE'), (12, 0.05, 'TRUE'), (12, 0.04, 'TRUE'), (15, 0.14, 'TRUE'), (18, 0.37, 'TRUE'), (18, 0.37, 'TRUE'), (21, 0.84, 'TRUE'), (24, 1.74, 'TRUE'), (24, 1.74, 'TRUE'), (27, 3.37, 'TRUE'), (30, 6.1, 'TRUE'), (30, 6.08, 'TRUE'), (33, 10.3, 'TRUE')], [(10, 0.02, 'FALSE'), (13, 0.07, 'FALSE'), (13, 0.07, 'FALSE'), (16, 0.2, 'FALSE'), (19, 0.5, 'FALSE'), (19, 0.5, 'FALSE'), (22, 1.08, 'FALSE'), (25, 2.21, 'FALSE'), (25, 2.21, 'FALSE'), (28, 4.19, 'FALSE'), (31, 7.33, 'FALSE'), (31, 7.3, 'FALSE'), (34, 12.1, 'FALSE')], [(10, 0.02, 'TRUE'), (12, 0.05, 'TRUE'), (14, 0.11, 'TRUE'), (16, 0.21, 'TRUE'), (18, 0.39, 'TRUE'), (20, 0.68, 'TRUE'), (22, 1.14, 'TRUE'), (24, 1.81, 'TRUE'), (26, 2.85, 'TRUE'), (28, 4.23, 'TRUE'), (30, 6.18, 'TRUE'), (32, 8.93, 'TRUE'), (34, 12.55, 'TRUE')], [(11, 0.03, 'FALSE'), (13, 0.07, 'FALSE'), (15, 0.15, 'FALSE'), (17, 0.29, 'FALSE'), (19, 0.52, 'FALSE'), (21, 0.88, 'FALSE'), (23, 1.46, 'FALSE'), (25, 2.29, 'FALSE'), (27, 3.45, 'FALSE'), (29, 5.17, 'FALSE'), (31, 7.43, 'FALSE'), (33, 10.63, 'FALSE')], [(11, 0.04, 'TRUE'), (13, 0.08, 'TRUE'), (15, 0.16, 'TRUE'), (17, 0.3, 'TRUE'), (19, 0.53, 'TRUE'), (21, 0.9, 'TRUE'), (23, 1.48, 'TRUE'), (25, 2.31, 'TRUE'), (27, 3.48, 'TRUE'), (29, 5.22, 'TRUE'), (31, 7.52, 'TRUE'), (33, 10.56, 'TRUE')], [(12, 0.05, 'FALSE'), (14, 0.12, 'FALSE'), (16, 0.22, 'FALSE'), (18, 0.41, 'FALSE'), (20, 0.72, 'FALSE'), (22, 1.16, 'FALSE'), (24, 1.85, 'FALSE'), (26, 2.83, 'FALSE'), (28, 4.24, 'FALSE'), (30, 6.26, 'FALSE'), (32, 9.04, 'FALSE'), (34, 12.64, 'FALSE')], [(8, 0.01, 'TRUE'), (12, 0.06, 'TRUE'), (12, 0.06, 'TRUE'), (16, 0.23, 'TRUE'), (16, 0.22, 'TRUE'), (20, 0.72, 'TRUE'), (20, 0.72, 'TRUE'), (24, 1.89, 'TRUE'), (24, 1.89, 'TRUE'), (28, 4.32, 'TRUE'), (28, 4.34, 'TRUE'), (32, 9.21, 'TRUE'), (32, 9.24, 'TRUE'), (36, 17.48, 'TRUE')], [(9, 0.02, 'FALSE'), (13, 0.08, 'FALSE'), (13, 0.08, 'FALSE'), (17, 0.3, 'FALSE'), (17, 0.3, 'FALSE'), (21, 0.92, 'FALSE'), (21, 0.91, 'FALSE'), (25, 2.36, 'FALSE'), (25, 2.35, 'FALSE'), (29, 5.31, 'FALSE'), (29, 5.34, 'FALSE'), (33, 10.77, 'FALSE')], [(10, 0.03, 'TRUE'), (12, 0.06, 'TRUE'), (14, 0.13, 'TRUE'), (16, 0.24, 'TRUE'), (18, 0.43, 'TRUE'), (20, 0.74, 'TRUE'), (22, 1.21, 'TRUE'), (24, 1.92, 'TRUE'), (26, 2.9, 'TRUE'), (28, 4.35, 'TRUE'), (30, 6.38, 'TRUE'), (32, 9.25, 'TRUE'), (34, 12.7, 'TRUE')], [(12, 0.07, 'FALSE'), (14, 0.13, 'FALSE'), (16, 0.24, 'FALSE'), (18, 0.44, 'FALSE'), (20, 0.74, 'FALSE'), (22, 1.3, 'FALSE'), (24, 1.95, 'FALSE'), (26, 2.99, 'FALSE'), (28, 4.46, 'FALSE'), (30, 6.53, 'FALSE'), (32, 9.11, 'FALSE'), (34, 12.71, 'FALSE')], [(10, 0.03, 'TRUE'), (12, 0.07, 'TRUE'), (14, 0.15, 'TRUE'), (16, 0.29, 'TRUE'), (18, 0.5, 'TRUE'), (20, 0.87, 'TRUE'), (22, 1.27, 'TRUE'), (24, 2.22, 'TRUE'), (26, 3.22, 'TRUE'), (28, 4.72, 'TRUE'), (30, 7.09, 'TRUE'), (32, 9.83, 'TRUE'), (34, 13.2, 'TRUE')], [(16, 0.26, 'FALSE'), (18, 0.48, 'FALSE'), (20, 0.78, 'FALSE'), (22, 1.32, 'FALSE'), (24, 2.03, 'FALSE'), (26, 3.08, 'FALSE'), (28, 4.69, 'FALSE'), (30, 6.81, 'FALSE'), (32, 9.48, 'FALSE'), (34, 13.44, 'FALSE')]]
for testIdx, tst in enumerate(data):
	lengths = []
	times = []

	for runIdx, run in enumerate(tst):
		lengths.append(run[0])
		times.append(run[1])

	plt.plot(lengths, times)
	plt.show()
