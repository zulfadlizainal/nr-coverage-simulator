# Created by github.com/zulfadlizainal

import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

#Ignore warning for heatmap legend
import logging
logging.getLogger().setLevel(logging.CRITICAL)

# Ignore warning if calculation devide by 'zero' or 'Nan'
np.seterr(divide='ignore', invalid='ignore')

df_antpat = pd.read_excel('Antenna_Pattern.xlsx')
df_cellparam = pd.read_excel('Cell_Parameter.xlsx')

# Create Indicators

split_H = df_antpat['ANTENNA_ELEMENT'].str.split('V', expand=True)
split_V = split_H.iloc[:, 1].str.split('(', expand=True)
HBeam = split_H.iloc[:, 0]
VBeam = 'V' + split_V.iloc[:, 0]
del split_H, split_V

# Create Info Table

cols = list(df_antpat.columns)
df_antpat_info = df_antpat[[cols[0]] +
                           [cols[2]] + [cols[1]] + [cols[5]] + [cols[4]]]
df_antpat_info = pd.concat([df_antpat_info, HBeam, VBeam], axis=1)
del cols, HBeam, VBeam

df_antpat_info.columns = ['Antenna Name', 'Vendor',
                          'Gain (dBi)', 'Etilt (°)', 'Pattern', 'HBW', 'VBW']
cols = list(df_antpat_info)
df_antpat_info = df_antpat_info[cols[0:4] + cols[5:7] + [cols[4]]]
df_antpat_display = df_antpat_info.loc[:, 'Antenna Name':'VBW']
del cols

# Print List of Antenna Patten

print(' ')
print('### List of Antenna Pattern Database ###')
print(' ')

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df_antpat_display)

print(' ')
print('### End of List ###')
print(' ')

# Mapping Cell_Parameter

height_cell_1 = df_cellparam.iloc[1, 1] - df_cellparam.iloc[0, 1]
height_cell_2 = df_cellparam.iloc[1, 2] - df_cellparam.iloc[0, 2]
height_cell_3 = df_cellparam.iloc[1, 3] - df_cellparam.iloc[0, 3]

azi_cell_1 = df_cellparam.iloc[2, 1]
azi_cell_2 = df_cellparam.iloc[2, 2]
azi_cell_3 = df_cellparam.iloc[2, 3]

mtilt_cell_1 = df_cellparam.iloc[3, 1]
mtilt_cell_2 = df_cellparam.iloc[3, 2]
mtilt_cell_3 = df_cellparam.iloc[3, 3]

ssbpower_cell_1 = df_cellparam.iloc[4, 1]
ssbpower_cell_2 = df_cellparam.iloc[4, 2]
ssbpower_cell_3 = df_cellparam.iloc[4, 3]

freq_cell_1 = df_cellparam.iloc[5, 1]
freq_cell_2 = df_cellparam.iloc[5, 2]
freq_cell_3 = df_cellparam.iloc[5, 3]

# Antenna Pattern Selection

pattern_cell_1 = int(input("Cell 1 Antenna Pattern: "))
pattern_cell_2 = int(input("Cell 2 Antenna Pattern: "))
pattern_cell_3 = int(input("Cell 3 Antenna Pattern: "))

####################################Cell 1 Preparation################################

# Prepare dataframe for selected antenna - Cell 1

antpat1 = df_antpat_info.loc[pattern_cell_1, 'Pattern']
antpat1 = antpat1.split(' ')
antpat1 = pd.DataFrame(antpat1)
antpat1.drop(antpat1.index[[0, 1, 2, 3, 724, 725,
                            726, 727, 1448, 1449, 1450]], inplace=True)
antpat1 = antpat1.reset_index(drop=True)

gain_cell_1 = df_antpat_info.loc[pattern_cell_1, 'Gain (dBi)']

# Seperate Horizontal and Vertical DataFrame - Cell 1

antpat_H1 = antpat1.iloc[0:720, :]
antpat_H1 = antpat_H1.reset_index(drop=True)
antpat_V1 = antpat1.iloc[720:1440, :]
antpat_V1 = antpat_V1.reset_index(drop=True)

antpat_H_Deg1 = antpat_H1.iloc[::2]  # Extract Odd Row Index DataFrame
antpat_H_Deg1 = antpat_H_Deg1.reset_index(drop=True)
antpat_H_Loss1 = antpat_H1.iloc[1::2]  # Extract Even Row Index Dataframe
antpat_H_Loss1 = antpat_H_Loss1.reset_index(drop=True)

antpat_V_Deg1 = antpat_V1.iloc[::2]  # Extract Odd Row Index DataFrame
antpat_V_Deg1 = antpat_V_Deg1.reset_index(drop=True)
antpat_V_Loss1 = antpat_V1.iloc[1::2]  # Extract Even Row Index Dataframe
antpat_V_Loss1 = antpat_V_Loss1.reset_index(drop=True)

antpat_df1 = pd.concat([antpat_H_Deg1, antpat_H_Loss1, antpat_V_Loss1], axis=1)
antpat_df1.columns = ['Angle', 'H_Loss', 'V_Loss']
antpat_df1['Angle'] = antpat_df1['Angle'].astype(int)
antpat_df1['H_Loss'] = antpat_df1['H_Loss'].astype(float)
antpat_df1['V_Loss'] = antpat_df1['V_Loss'].astype(float)

cols = list(antpat_df1)
antpat_df_H_Cell_1 = antpat_df1[cols[0:2]]
antpat_df_V_Cell_1 = antpat_df1[cols[0:1] + [cols[2]]]

del cols, antpat1, antpat_H1, antpat_H_Deg1, antpat_H_Loss1, antpat_V1, antpat_V_Deg1, antpat_V_Loss1, antpat_df1

# Shift dataframe based on Azimuth and Tilt - Cell 1

hloss_cell_1 = antpat_df_H_Cell_1['H_Loss'].tolist()
vloss_cell_1 = antpat_df_V_Cell_1['V_Loss'].tolist()


def rotate(l, n):
    return l[-n:] + l[:-n]


hloss_cell_1 = rotate(hloss_cell_1, azi_cell_1)
vloss_cell_1 = rotate(vloss_cell_1, mtilt_cell_1)

del antpat_df_H_Cell_1, antpat_df_V_Cell_1

####################################Cell 2 Preparation################################

# Prepare dataframe for selected antenna - Cell 2

antpat2 = df_antpat_info.loc[pattern_cell_2, 'Pattern']
antpat2 = antpat2.split(' ')
antpat2 = pd.DataFrame(antpat2)
antpat2.drop(antpat2.index[[0, 1, 2, 3, 724, 725,
                            726, 727, 1448, 1449, 1450]], inplace=True)
antpat2 = antpat2.reset_index(drop=True)

gain_cell_2 = df_antpat_info.loc[pattern_cell_2, 'Gain (dBi)']

# Seperate Horizontal and Vertical DataFrame - Cell 2

antpat_H2 = antpat2.iloc[0:720, :]
antpat_H2 = antpat_H2.reset_index(drop=True)
antpat_V2 = antpat2.iloc[720:1440, :]
antpat_V2 = antpat_V2.reset_index(drop=True)

antpat_H_Deg2 = antpat_H2.iloc[::2]  # Extract Odd Row Index DataFrame
antpat_H_Deg2 = antpat_H_Deg2.reset_index(drop=True)
antpat_H_Loss2 = antpat_H2.iloc[1::2]  # Extract Even Row Index Dataframe
antpat_H_Loss2 = antpat_H_Loss2.reset_index(drop=True)

antpat_V_Deg2 = antpat_V2.iloc[::2]  # Extract Odd Row Index DataFrame
antpat_V_Deg2 = antpat_V_Deg2.reset_index(drop=True)
antpat_V_Loss2 = antpat_V2.iloc[1::2]  # Extract Even Row Index Dataframe
antpat_V_Loss2 = antpat_V_Loss2.reset_index(drop=True)

antpat_df2 = pd.concat([antpat_H_Deg2, antpat_H_Loss2, antpat_V_Loss2], axis=1)
antpat_df2.columns = ['Angle', 'H_Loss', 'V_Loss']
antpat_df2['Angle'] = antpat_df2['Angle'].astype(int)
antpat_df2['H_Loss'] = antpat_df2['H_Loss'].astype(float)
antpat_df2['V_Loss'] = antpat_df2['V_Loss'].astype(float)

cols = list(antpat_df2)
antpat_df_H_Cell_2 = antpat_df2[cols[0:2]]
antpat_df_V_Cell_2 = antpat_df2[cols[0:1] + [cols[2]]]

del cols, antpat2, antpat_H2, antpat_H_Deg2, antpat_H_Loss2, antpat_V2, antpat_V_Deg2, antpat_V_Loss2, antpat_df2

# Shift dataframe based on Azimuth and Tilt - Cell 2

hloss_cell_2 = antpat_df_H_Cell_2['H_Loss'].tolist()
vloss_cell_2 = antpat_df_V_Cell_2['V_Loss'].tolist()


def rotate(l, n):
    return l[-n:] + l[:-n]


hloss_cell_2 = rotate(hloss_cell_2, azi_cell_2)
vloss_cell_2 = rotate(vloss_cell_2, mtilt_cell_2)

del antpat_df_H_Cell_2, antpat_df_V_Cell_2


####################################Cell 3 Preparation################################

# Prepare dataframe for selected antenna - Cell 3

antpat3 = df_antpat_info.loc[pattern_cell_3, 'Pattern']
antpat3 = antpat3.split(' ')
antpat3 = pd.DataFrame(antpat3)
antpat3.drop(antpat3.index[[0, 1, 2, 3, 724, 725,
                            726, 727, 1448, 1449, 1450]], inplace=True)
antpat3 = antpat3.reset_index(drop=True)

gain_cell_3 = df_antpat_info.loc[pattern_cell_3, 'Gain (dBi)']

# Seperate Horizontal and Vertical DataFrame - Cell 3

antpat_H3 = antpat3.iloc[0:720, :]
antpat_H3 = antpat_H3.reset_index(drop=True)
antpat_V3 = antpat3.iloc[720:1440, :]
antpat_V3 = antpat_V3.reset_index(drop=True)

antpat_H_Deg3 = antpat_H3.iloc[::2]  # Extract Odd Row Index DataFrame
antpat_H_Deg3 = antpat_H_Deg3.reset_index(drop=True)
antpat_H_Loss3 = antpat_H3.iloc[1::2]  # Extract Even Row Index Dataframe
antpat_H_Loss3 = antpat_H_Loss3.reset_index(drop=True)

antpat_V_Deg3 = antpat_V3.iloc[::2]  # Extract Odd Row Index DataFrame
antpat_V_Deg3 = antpat_V_Deg3.reset_index(drop=True)
antpat_V_Loss3 = antpat_V3.iloc[1::2]  # Extract Even Row Index Dataframe
antpat_V_Loss3 = antpat_V_Loss3.reset_index(drop=True)

antpat_df3 = pd.concat([antpat_H_Deg3, antpat_H_Loss3, antpat_V_Loss3], axis=1)
antpat_df3.columns = ['Angle', 'H_Loss', 'V_Loss']
antpat_df3['Angle'] = antpat_df3['Angle'].astype(int)
antpat_df3['H_Loss'] = antpat_df3['H_Loss'].astype(float)
antpat_df3['V_Loss'] = antpat_df3['V_Loss'].astype(float)

cols = list(antpat_df3)
antpat_df_H_Cell_3 = antpat_df3[cols[0:2]]
antpat_df_V_Cell_3 = antpat_df3[cols[0:1] + [cols[2]]]

del cols, antpat3, antpat_H3, antpat_H_Deg3, antpat_H_Loss3, antpat_V3, antpat_V_Deg3, antpat_V_Loss3, antpat_df3

# Shift dataframe based on Azimuth and Tilt - Cell 3

hloss_cell_3 = antpat_df_H_Cell_3['H_Loss'].tolist()
vloss_cell_3 = antpat_df_V_Cell_3['V_Loss'].tolist()


def rotate(l, n):
    return l[-n:] + l[:-n]


hloss_cell_3 = rotate(hloss_cell_3, azi_cell_3)
vloss_cell_3 = rotate(vloss_cell_3, mtilt_cell_3)

del antpat_df_H_Cell_3, antpat_df_V_Cell_3

#######################################Clear Memory#################################

del df_antpat, df_antpat_display, df_antpat_info, df_cellparam

####################################Mesh Calculation################################

# Define mesh radius in meters
grid = 600
step = 10

# Create Matrix based on Radius
col = np.arange(start=grid, stop=0 - step, step=-step)
idx = np.arange(start=grid, stop=0 - step, step=-step)
idx_ones = np.ones(int(grid / step) + 1)

col = col.reshape(int(grid / step) + 1, 1)  # Change Matrix

# Create 1/4 Mesh Based on Matrix
# Flat Distance from Center Point
distance_flat = np.sqrt((np.power(col, 2)) + (np.power(idx, 2)))
col_dis = col * idx_ones  # Dummy distance towards straight Lines

# Horizontal Angle from Center Point
angle_H = np.rad2deg(np.arcsin(col_dis / distance_flat))
angle_H = np.round(angle_H)  # Round the angle

# Hypotenuse Distance from Cell Height (Cell 1)
distance_hp_1 = np.sqrt((np.power(distance_flat, 2)) +
                        (np.power(height_cell_1, 2)))
# Hypotenuse Distance from Cell Height (Cell 2)
distance_hp_2 = np.sqrt((np.power(distance_flat, 2)) +
                        (np.power(height_cell_2, 2)))
# Hypotenuse Distance from Cell Height (Cell 3)
distance_hp_3 = np.sqrt((np.power(distance_flat, 2)) +
                        (np.power(height_cell_2, 2)))

# Vertical Angle from Center Point (Cell 1)
angle_V_1 = 90 - np.rad2deg(np.arcsin(distance_flat / distance_hp_1))
angle_V_1 = np.round(angle_V_1)  # Round the angle
# Vertical Angle from Center Point (Cell 2)
angle_V_2 = 90 - np.rad2deg(np.arcsin(distance_flat / distance_hp_2))
angle_V_2 = np.round(angle_V_2)  # Round the angle
# Vertical Angle from Center Point (Cell 3)
angle_V_3 = 90 - np.rad2deg(np.arcsin(distance_flat / distance_hp_3))
angle_V_3 = np.round(angle_V_3)  # Round the angle

# Calculate Path Loss Model - Measurement based model (3.5GHz)

mb_pl_1 = ((5*(10**(-7)))*(distance_hp_1**3)) - ((0.0005)*(distance_hp_1**2)) + ((0.2469)*(distance_hp_1)) + 107.6 # Path Loss for Cell 1
mb_pl_2 = ((5*(10**(-7)))*(distance_hp_2**3)) - ((0.0005)*(distance_hp_2**2)) + ((0.2469)*(distance_hp_2)) + 107.6 # Path Loss for Cell 1
mb_pl_3 = ((5*(10**(-7)))*(distance_hp_3**3)) - ((0.0005)*(distance_hp_3**2)) + ((0.2469)*(distance_hp_3)) + 107.6 # Path Loss for Cell 1

del col, col_dis, idx, idx_ones
del distance_flat, distance_hp_1, distance_hp_2, distance_hp_3

####################################Create Full Mesh################################

######Path Loss (Cell 1)######

# Flip Path Loss
mb_pl_1_NE = np.flip(mb_pl_1, axis=1)

# Prepare Dataframe
mb_pl_1 = pd.DataFrame(mb_pl_1)  # Convert array to Dataframe

mb_pl_1_NE = pd.DataFrame(mb_pl_1_NE)  # Convert array to Dataframe
mb_pl_1_NE = mb_pl_1_NE.iloc[:, 1:]  # Remove redundant columns

mb_pl_1 = pd.concat([mb_pl_1, mb_pl_1_NE], axis=1,
                    sort=False)  # First half of the Mesh
mb_pl_1_S = mb_pl_1.values  # Switch to array because dataframe cannot flip
mb_pl_1_S = np.flip(mb_pl_1_S, axis=0)  # Create 2nd half of the Mesh
mb_pl_1_S = pd.DataFrame(mb_pl_1_S)
mb_pl_1_S = mb_pl_1_S.iloc[1:, :]

# Standardize column 1st and 2nd half of the Mesh
mb_pl_1.columns = mb_pl_1_S.columns

mb_pl_1 = pd.concat([mb_pl_1, mb_pl_1_S], axis=0,
                    sort=False)  # Form a complete mesh grid
mb_pl_1 = mb_pl_1.reset_index(drop=True)

del mb_pl_1_NE, mb_pl_1_S

######Path Loss (Cell 2)######

# Flip Path Loss
mb_pl_2_NE = np.flip(mb_pl_2, axis=1)

# Prepare Dataframe
mb_pl_2 = pd.DataFrame(mb_pl_2)  # Convert array to Dataframe

mb_pl_2_NE = pd.DataFrame(mb_pl_2_NE)  # Convert array to Dataframe
mb_pl_2_NE = mb_pl_2_NE.iloc[:, 1:]  # Remove redundant columns

mb_pl_2 = pd.concat([mb_pl_2, mb_pl_2_NE], axis=1,
                    sort=False)  # First half of the Mesh
mb_pl_2_S = mb_pl_2.values  # Switch to array because dataframe cannot flip
mb_pl_2_S = np.flip(mb_pl_2_S, axis=0)  # Create 2nd half of the Mesh
mb_pl_2_S = pd.DataFrame(mb_pl_2_S)
mb_pl_2_S = mb_pl_2_S.iloc[1:, :]

# Standardize column 1st and 2nd half of the Mesh
mb_pl_2.columns = mb_pl_2_S.columns

mb_pl_2 = pd.concat([mb_pl_2, mb_pl_2_S], axis=0,
                    sort=False)  # Form a complete mesh grid
mb_pl_2 = mb_pl_2.reset_index(drop=True)

del mb_pl_2_NE, mb_pl_2_S

######Path Loss (Cell 3)######

# Flip Path Loss
mb_pl_3_NE = np.flip(mb_pl_3, axis=1)

# Prepare Dataframe
mb_pl_3 = pd.DataFrame(mb_pl_3)  # Convert array to Dataframe

mb_pl_3_NE = pd.DataFrame(mb_pl_3_NE)  # Convert array to Dataframe
mb_pl_3_NE = mb_pl_3_NE.iloc[:, 1:]  # Remove redundant columns

mb_pl_3 = pd.concat([mb_pl_3, mb_pl_3_NE], axis=1,
                    sort=False)  # First half of the Mesh
mb_pl_3_S = mb_pl_3.values  # Switch to array because dataframe cannot flip
mb_pl_3_S = np.flip(mb_pl_3_S, axis=0)  # Create 2nd half of the Mesh
mb_pl_3_S = pd.DataFrame(mb_pl_3_S)
mb_pl_3_S = mb_pl_3_S.iloc[1:, :]

# Standardize column 1st and 2nd half of the Mesh
mb_pl_3.columns = mb_pl_3_S.columns

mb_pl_3 = pd.concat([mb_pl_3, mb_pl_3_S], axis=0,
                    sort=False)  # Form a complete mesh grid
mb_pl_3 = mb_pl_3.reset_index(drop=True)

del mb_pl_3_NE, mb_pl_3_S


######Horizontal Degree Mesh (All Cell)######

# Rotate and Flip Horizontal Degree
angle_H_NE = np.rot90(angle_H)
angle_H_NE = np.flip(angle_H_NE, axis=0)
angle_H_NE = np.flip(angle_H_NE, axis=1)

angle_H_SE = np.rot90(angle_H_NE, 3)
angle_H_SE = angle_H_SE + 90

angle_H_SW = np.rot90(angle_H_SE, 3)
angle_H_SW = angle_H_SW + 90

angle_H_NW = np.rot90(angle_H_SW, 3)
angle_H_NW = angle_H_NW + 90

# Prepare Dataframe
angle_H_NE = pd.DataFrame(angle_H_NE)
angle_H_SE = pd.DataFrame(angle_H_SE)
angle_H_SW = pd.DataFrame(angle_H_SW)
angle_H_NW = pd.DataFrame(angle_H_NW)
angle_H_SE = angle_H_SE.iloc[1:, :]
angle_H_SW = angle_H_SW.iloc[1:, :-1]
angle_H_NW = angle_H_NW.iloc[:, :-1]

# Combine Dataframe to become Mesh
angle_H_N = pd.concat([angle_H_NW, angle_H_NE], axis=1, sort=False)
angle_H_N = angle_H_N.values
angle_H_N = pd.DataFrame(angle_H_N)

angle_H_S = pd.concat([angle_H_SW, angle_H_SE], axis=1, sort=False)
angle_H_S = angle_H_S.values
angle_H_S = pd.DataFrame(angle_H_S)

angle_H = pd.concat([angle_H_N, angle_H_S], axis=0, sort=False)
angle_H = angle_H.values
angle_H = pd.DataFrame(angle_H)
angle_H = angle_H.fillna(0)

del angle_H_N, angle_H_S, angle_H_NE, angle_H_SE, angle_H_SW, angle_H_NW


######Horizontal Loss Mesh (All Cell)######

# Cell 1 - Horizontal Loss
hloss_mesh_cell_1 = angle_H.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_H)):
    j = 0
    for j in range(len(angle_H)):
        temp = angle_H[i][j]
        temp = temp.astype(np.int64)
        hloss_mesh_cell_1[i][j] = hloss_cell_1[temp]

del temp, i, j

# Cell 2 - Horizontal Loss
hloss_mesh_cell_2 = angle_H.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_H)):
    j = 0
    for j in range(len(angle_H)):
        temp = angle_H[i][j]
        temp = temp.astype(np.int64)
        hloss_mesh_cell_2[i][j] = hloss_cell_2[temp]

del temp, i, j

# Cell 3 - Horizontal Loss
hloss_mesh_cell_3 = angle_H.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_H)):
    j = 0
    for j in range(len(angle_H)):
        temp = angle_H[i][j]
        temp = temp.astype(np.int64)
        hloss_mesh_cell_3[i][j] = hloss_cell_3[temp]

del temp, i, j


######Vertical Degree Mesh (All Cell)######

# Cell 1

# Rotate and Flip Vertical Degree

angle_V_1_NW = angle_V_1
angle_V_1_NE = np.flip(angle_V_1_NW, axis=1)
angle_V_1_SW = np.flip(angle_V_1_NW, axis=0)
angle_V_1_SE = np.flip(angle_V_1_NE, axis=0)

# Prepare Dataframe
angle_V_1_NE = pd.DataFrame(angle_V_1_NE)
angle_V_1_SE = pd.DataFrame(angle_V_1_SE)
angle_V_1_SW = pd.DataFrame(angle_V_1_SW)
angle_V_1_NW = pd.DataFrame(angle_V_1_NW)
angle_V_1_SE = angle_V_1_SE.iloc[1:, :]
angle_V_1_SW = angle_V_1_SW.iloc[1:, :-1]
angle_V_1_NW = angle_V_1_NW.iloc[:, :-1]

# Combine Dataframe to become Mesh
angle_V_1_N = pd.concat([angle_V_1_NW, angle_V_1_NE], axis=1, sort=False)
angle_V_1_N = angle_V_1_N.values
angle_V_1_N = pd.DataFrame(angle_V_1_N)

angle_V_1_S = pd.concat([angle_V_1_SW, angle_V_1_SE], axis=1, sort=False)
angle_V_1_S = angle_V_1_S.values
angle_V_1_S = pd.DataFrame(angle_V_1_S)

angle_V_1 = pd.concat([angle_V_1_N, angle_V_1_S], axis=0, sort=False)
angle_V_1 = angle_V_1.values
angle_V_1 = pd.DataFrame(angle_V_1)
angle_V_1 = angle_V_1.fillna(0)

del angle_V_1_N, angle_V_1_S, angle_V_1_NE, angle_V_1_SE, angle_V_1_SW, angle_V_1_NW

# Cell 2

# Rotate and Flip Vertical Degree

angle_V_2_NW = angle_V_2
angle_V_2_NE = np.flip(angle_V_2_NW, axis=1)
angle_V_2_SW = np.flip(angle_V_2_NW, axis=0)
angle_V_2_SE = np.flip(angle_V_2_NE, axis=0)

# Prepare Dataframe
angle_V_2_NE = pd.DataFrame(angle_V_2_NE)
angle_V_2_SE = pd.DataFrame(angle_V_2_SE)
angle_V_2_SW = pd.DataFrame(angle_V_2_SW)
angle_V_2_NW = pd.DataFrame(angle_V_2_NW)
angle_V_2_SE = angle_V_2_SE.iloc[1:, :]
angle_V_2_SW = angle_V_2_SW.iloc[1:, :-1]
angle_V_2_NW = angle_V_2_NW.iloc[:, :-1]

# Combine Dataframe to become Mesh
angle_V_2_N = pd.concat([angle_V_2_NW, angle_V_2_NE], axis=1, sort=False)
angle_V_2_N = angle_V_2_N.values
angle_V_2_N = pd.DataFrame(angle_V_2_N)

angle_V_2_S = pd.concat([angle_V_2_SW, angle_V_2_SE], axis=1, sort=False)
angle_V_2_S = angle_V_2_S.values
angle_V_2_S = pd.DataFrame(angle_V_2_S)

angle_V_2 = pd.concat([angle_V_2_N, angle_V_2_S], axis=0, sort=False)
angle_V_2 = angle_V_2.values
angle_V_2 = pd.DataFrame(angle_V_2)
angle_V_2 = angle_V_2.fillna(0)

del angle_V_2_N, angle_V_2_S, angle_V_2_NE, angle_V_2_SE, angle_V_2_SW, angle_V_2_NW

# Cell 3

# Rotate and Flip Vertical Degree

angle_V_3_NW = angle_V_3
angle_V_3_NE = np.flip(angle_V_3_NW, axis=1)
angle_V_3_SW = np.flip(angle_V_3_NW, axis=0)
angle_V_3_SE = np.flip(angle_V_3_NE, axis=0)

# Prepare Dataframe
angle_V_3_NE = pd.DataFrame(angle_V_3_NE)
angle_V_3_SE = pd.DataFrame(angle_V_3_SE)
angle_V_3_SW = pd.DataFrame(angle_V_3_SW)
angle_V_3_NW = pd.DataFrame(angle_V_3_NW)
angle_V_3_SE = angle_V_3_SE.iloc[1:, :]
angle_V_3_SW = angle_V_3_SW.iloc[1:, :-1]
angle_V_3_NW = angle_V_3_NW.iloc[:, :-1]

# Combine Dataframe to become Mesh
angle_V_3_N = pd.concat([angle_V_3_NW, angle_V_3_NE], axis=1, sort=False)
angle_V_3_N = angle_V_3_N.values
angle_V_3_N = pd.DataFrame(angle_V_3_N)

angle_V_3_S = pd.concat([angle_V_3_SW, angle_V_3_SE], axis=1, sort=False)
angle_V_3_S = angle_V_3_S.values
angle_V_3_S = pd.DataFrame(angle_V_3_S)

angle_V_3 = pd.concat([angle_V_3_N, angle_V_3_S], axis=0, sort=False)
angle_V_3 = angle_V_3.values
angle_V_3 = pd.DataFrame(angle_V_3)
angle_V_3 = angle_V_3.fillna(0)

del angle_V_3_N, angle_V_3_S, angle_V_3_NE, angle_V_3_SE, angle_V_3_SW, angle_V_3_NW


######Vertical Loss Mesh (All Cell)######

# Cell 1 - Vertical Loss
vloss_mesh_cell_1 = angle_V_1.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_V_1)):
    j = 0
    for j in range(len(angle_V_1)):
        temp = angle_V_1[i][j]
        temp = temp.astype(np.int64)
        vloss_mesh_cell_1[i][j] = vloss_cell_1[temp]

del temp, i, j


# Cell 2 - Vertical Loss
vloss_mesh_cell_2 = angle_V_2.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_V_2)):
    j = 0
    for j in range(len(angle_V_2)):
        temp = angle_V_2[i][j]
        temp = temp.astype(np.int64)
        vloss_mesh_cell_2[i][j] = vloss_cell_2[temp]

del temp, i, j


# Cell 3 - Vertical Loss
vloss_mesh_cell_3 = angle_V_3.copy()
temp = pd.Series([])

i = 0
j = 0

for i in range(len(angle_V_3)):
    j = 0
    for j in range(len(angle_V_3)):
        temp = angle_V_3[i][j]
        temp = temp.astype(np.int64)
        vloss_mesh_cell_3[i][j] = vloss_cell_3[temp]

del temp, i, j


######Final RSRP Mesh (All Cell)######

#Total loss Cell 1, 2, and 3
tloss_mesh_cell_1 = mb_pl_1 + hloss_mesh_cell_1 + vloss_mesh_cell_1
tloss_mesh_cell_2 = mb_pl_2 + hloss_mesh_cell_2 + vloss_mesh_cell_2
tloss_mesh_cell_3 = mb_pl_3 + hloss_mesh_cell_3 + vloss_mesh_cell_3

#RSRP Cell 1, 2, and 3
rsrp_mesh_cell_1 = ssbpower_cell_1 + gain_cell_1 - tloss_mesh_cell_1
rsrp_mesh_cell_2 = ssbpower_cell_2 + gain_cell_2 - tloss_mesh_cell_2
rsrp_mesh_cell_3 = ssbpower_cell_3 + gain_cell_3 - tloss_mesh_cell_3

#Convet DF to Numpy Array
rsrp_mesh_cell_1 = rsrp_mesh_cell_1.to_numpy()
rsrp_mesh_cell_2 = rsrp_mesh_cell_2.to_numpy()
rsrp_mesh_cell_3 = rsrp_mesh_cell_3.to_numpy()

#Pick Max value in every mesh
rsrp_mesh = np.maximum.reduce([rsrp_mesh_cell_1, rsrp_mesh_cell_2, rsrp_mesh_cell_3])

#Remove out of range samples
rsrp_mesh_cell_1[rsrp_mesh_cell_1 < -140] = np.nan
rsrp_mesh_cell_2[rsrp_mesh_cell_2 < -140] = np.nan
rsrp_mesh_cell_3[rsrp_mesh_cell_3 < -140] = np.nan
rsrp_mesh[rsrp_mesh < -140] = np.nan

#Change numpy array to pandas dataframe
rsrp_mesh_cell_1 = pd.DataFrame(rsrp_mesh_cell_1)
rsrp_mesh_cell_2 = pd.DataFrame(rsrp_mesh_cell_2)
rsrp_mesh_cell_3 = pd.DataFrame(rsrp_mesh_cell_3)
rsrp_mesh = pd.DataFrame(rsrp_mesh)


######Plot RSRP Map######

plt.imshow(rsrp_mesh, cmap='RdYlGn', interpolation='hermite', vmin = -140, vmax = -90, extent=[grid*(-1), grid, grid*(-1), grid])

#plt.colorbar()

plt.xlabel("Distance (m)")
plt.ylabel("Distance (m)")

ax = plt.gca()
ax.set_xticks(np.arange(grid*(-1), grid, (step*20)))
ax.set_yticks(np.arange(grid*(-1), grid, (step*20)))

plt.title("5G Coverage Map\nSS-RSRP - Measurement Based PL Model [3.9GHz]\n")
plt.grid(which='major', axis='both', linestyle='--')

plt.colorbar()
plt.legend(title="SS-RSRP (dBm)", loc='lower right')

plt.show()


######Processing Time######

time = time.process_time()
print(f'\nProcessing Time: {time} secs')


#End
print(' ')
print('ありがとうございました！！')
print('Download this program: https://github.com/zulfadlizainal')
print('Author: https://www.linkedin.com/in/zulfadlizainal')
print(' ')
