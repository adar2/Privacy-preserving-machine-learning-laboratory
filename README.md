# Privacy Preserving Log-Rank Test – analysis and implementation


**Abstract**

The Python-based implementation details and results of the ASY Protocol: A privacy preserving protocol that securely computes an approximation for the Log-Rank test without risking exposure of valuable data. Our implementation is included as part of our ASY Protocol1 PC application, which supports MPC computation and results view with an accessible and easy to use interface. The implementation uses Paillier2 additive homomorphic encryption for Multi Party Computation (MPC) and HTTPS based communication between the Client, Data Server, and Security Server. An empirical evaluation of the protocol was run using our software and results show that regardless of the dataset size, the difference between Z\* (the result of an ASY Protocol MPC calculation) and Z (standard Log-Rank test result) can be capped by ϵ.

**1. Software Overview**

Our application was written in Python and acts as a fully fuinctional PC Application. After installation, the application is run by the user and has 4 basic functionalities: Create a new experiment, Upload data to an existing experiment, view the current results of an existing experiment and run simulations.

![image](https://user-images.githubusercontent.com/63145449/174775238-3791be45-cc48-4adc-ab83-3e44229c7a85.png)

_1.1 Create a new experiment_

After selecting &quot;Create New Experiment&quot;, the user only has to provide the experiment&#39;s name. He is then provided with a Unique ID, with which other parties will be able to participate in the experiment with their own data. When creating a new experiment, a public key and private key are generated using the Security server and are associated with the experiment. The public key is stored in the Data Server along with the encrypted results, and the private key is stored in the Securiy Server, with which results are decrypted.

_1.2 Upload Data_

After selecting &quot;Upload Data&quot;, the user has to provide the desired experiment&#39;s Unique ID and the data he wishes to add to it. The software runs an ASY protocol on the selected Data file, encrypts it with the public key that is associated with the experiment and then sends the encrypted results to the Data Server.

_1.2.1 ASY Protocol implementation_

The application runs an ASY protocol calculation on the data. The protocol was implemented using pseudo-code included in our project materials.

_1.3 View Results_

After selecting &quot;View Results&quot;, the user only has to provide the desired experiment&#39;s Unique ID. If a valid ID was entered, the current result of the experiment (Z\*) is shown on a popup screen. The encrypted results are stored in the Data Server, but the results shown to the user are final results that have gone through decryption using the Security server.

_1.4 Simulations_

After selecting &quot;Simulations&quot;, the user is presented with a form, in which he has to fill the required parameters for the simlations: The number of parties to be used in the MPC, The number of runs he wishes to perform and the number of patients to be used, if generated dataset is to be used. The user can also upload his own Data file, in which case the number of patients is not used. The user then needs to select &quot;Run Simulations&quot;.

After the simulations are performed, 2 graphs are shown: A simple step-function graph to describe the regular Log-Rank test and its result, Z, and a histogram to show the difference between the regular Log-Rank test results – Z - and the ASY Protocol MPC result – Z\*.

![image](https://user-images.githubusercontent.com/63145449/174775256-9126ded6-e92c-4f05-ab41-d48c468ff8cd.png)

_1.5 Communication_

The Client, Data Server and Security Server all communicate via secure HTTPS requests. Requests are made one at a time and on demand.

The Data Server holds a database of experiments, and each record contains: Experiment name, Unique ID, Start date, Public Key (Given by the security server when the experiment is created) and the current encrypted result.

The Security Server holds a dabase of experiments as well, but each record only contains the Unique ID of an experiment and a private key, which is used to decrypt it&#39;s reults.

_1.6 Encryption_

The encryption used for the MPC is Additive Homomorphic Paillier Encryption. The implementation of the Paillier algorithm is taken from the python-paillier package3.

**2. Results**

Using the Simulations mechanism implemented in our software, we are able to produce an empirical evaluation of the ASY Protocol performance compared to the standard Log-Rank test&#39;s performance.

_2.1 Statistical Accuracy_

Below are histograms showing the difference between the results of both algortihms with different parameters: number of runs, number of patients and number of parties.

First, we observe results for 250 patients for data size with varying sizes of parties.

![image](https://user-images.githubusercontent.com/63145449/174775301-852005d3-4681-4ef5-9410-41c2c1738de5.png)

![image](https://user-images.githubusercontent.com/63145449/174775331-81e9d821-fb74-4248-9c80-0a9ef6ebc163.png)

![image](https://user-images.githubusercontent.com/63145449/174775344-3b0a19b2-9966-4a23-92a6-0661950efee2.png)

Then, we observe the same party variance for data size of 100:

![image](https://user-images.githubusercontent.com/63145449/174775358-7343b72f-4036-428a-ab54-415f297624a0.png)

![image](https://user-images.githubusercontent.com/63145449/174775384-75c6bd3a-2baa-404f-8bbe-cd53e9bcfd0b.png)

![image](https://user-images.githubusercontent.com/63145449/174775404-4dcf2644-94c8-491b-a57d-46f4f47e54e0.png)

An empirical evaluation of our results show high statistical accuracy when performing the ASY protocol MPC in contrast with the standard LogRank test. Data size and party count influence the difference between the two, and it is possible to cap the difference for each party size and data size variation.

_2.2 Time Efficiency_

Below are graphs describing the time differences of both algorithms:

![image](https://user-images.githubusercontent.com/63145449/174775425-c26f1eb4-b23a-4d26-9a45-1acc727e85dc.png)

![image](https://user-images.githubusercontent.com/63145449/174775441-01004c37-2fd4-4b8f-afc0-6e3da0ea3d87.png)

!![image](https://user-images.githubusercontent.com/63145449/174775463-87ea0fba-0525-4e52-aa74-bfc815f05b87.png)

The ASY Protocol, as expected, takes considerably more time to perform than the standard LogRank test. Note that the ASY Protocol runs use local MPC, and for real life usage, communication time may have a varying impact on the results.

_2.3 Memory Efficiency_

Neither algorithm takes much memory to run. Throughout our simulations, the LogRank run peak memory use was 600 KBs, while the ASY Protocol peak memory use was 1.15 MBs. The ASY Protocol does take more memory to perform, but both peaks are very low and any modern hardware will handle the memory signature with ease.

**References**

1. A privacy preserving protocol that securely computes an (approximation for the) logrank test was recently developed by Akavia, Samohi and Yakhini [ASY]
2. [https://en.wikipedia.org/wiki/Paillier\_cryptosystem](https://en.wikipedia.org/wiki/Paillier_cryptosystem)
3. [https://python-paillier.readthedocs.io/en/develop/#](https://python-paillier.readthedocs.io/en/develop/#)
