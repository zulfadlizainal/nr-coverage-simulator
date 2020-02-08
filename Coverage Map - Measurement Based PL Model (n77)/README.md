# Coverage Map - Measurement Based PL Model (n77)

This simulation is derived from actual measurement data of live 5G NR site in band n77. The path loss model is created by reverse calculating the actual SS-RSRP measurement by considering the antenna pattern and actual site configuration of the live site.

### Explanation

The basic concept of path loss model is explained here ([Link](https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/tree/master/Coverage%20Map%20-%20Free%20Space%20PL%20Model)). However, the accuracy is fallen far from good. Hence, this model will try to utilize the actual measurement data of 5G NR aiming to improves accuracy to the prediction.

### Path Loss Model

The method that I use to create measurement based PL model are listed as follows:
<br />
1. Measure 5G NR SS-RSRP at several locations with GPS information attached.
2. Calculate the distance of every collected samples from the serving 5G NR gNB.
3. Derive actual path loss from every samples by considering SSB Power, Antenna Gain, and Antenna Pattern.
4. Derive a polynomial equation that represents path loss and distance as below chart.
<br />
Testing Setup:
<br />
<br />
Tech: 5G NR NSA
<br />
Band: n77 3.9GHz
<br />
SSB Power: 15dBm
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/MBPLN77_Explain1.png" alt="n77 MBPL" title="n77 MBPL" width=100% height=100% />
<br />
<br />

### Results

Expected result shows the SS-RSRP based on the distance from implemented cell. If you perform any input parameter changes, it will give you and idea what your 5G coverage will look like. This model is only True if the 5G NR coverage is on band n77.
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/MBPLN77_Result1.png" alt="FSPL vs MBPL" title="FSPL vs MBPL" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/5G-NR-Coverage-Prediction/blob/master/img/MBPLN77_Result2.png.png" alt="Tilt Change" title="Tilt Change" width=100% height=100% />
<br />
<br />
