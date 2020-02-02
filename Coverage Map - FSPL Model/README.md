# Coverage Map - Free Space Path Loss Model

This simulation is based on Free Space Path Loss model to estimate the SS-RSRP coverage in 5G NR. Few possibilities of configuration can be set to understand the impact of any RF parameter tuning to the coverage.

### Explanation
The simulation is considering link gain and loss factors in 5G NR implementation. Parameters to be considered in this simulation is: Antenna Gain, Antenna Pattern (HLoss & VLoss), SSB Tx Power, and Path Loss Model (Antenna Height, UE Height, Channel Model, and Distance). The main goal is to estimate the SS-RSRP coverage level.

Basic link diagram:
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_Concept.png" alt="Link" title="Link" width=100% height=100% />
<br />
<br />
Antenna pattern loss in H Plane and V Plane is being considered:
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_AntPat.png" alt="Ant Pattern" title="Ant Pattern" width=100% height=100% />
<br />
<br />
Image of antenna pattern radiation and loss:
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_AntRad.png" alt="Ant radiation" title="Ant radiation" width=100% height=100% />
<br />

### Path Loss Model

Free space path loss model is being considered for this simulation calculation. Below snapshot from Wiki.
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_Model.png" alt="FSPL Model" title="FSPL Model" width=100% height=100% />
<br />
<br />

### Results

Expected result shows the SS-RSRP based on the distance from implemented cell. If you perform any input parameter changes, it will give you and idea what your 5G coverage will look like.
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_Result1.png" alt="Azimuth Change" title="Azimuth Change" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_Result2.png" alt="Tilt Change" title="Tilt Change" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/FSPL_Result3.png" alt="Beamwidth Change" title="Beamwidth Change" width=100% height=100% />
<br />
<br />
