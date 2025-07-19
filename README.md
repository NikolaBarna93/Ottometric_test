This repository contains 2 automated test cases for Ottometric using Selenium and Python

Test1 (Checking if average percentage is calculated correctly)

1. Launch brawser and navigate to https://qa-ottoviz.ominf.net/
2. Log in using the provided test credentials
3. Select program "Camera System VI1"
4. Navigate to KPM Sensor -> FCM -> Lanes
5. For each column calculate average percentage
6. Compare calculated value with value from footer
7. Write results in report file
8. Close brawser

Test2 (Counting ENV events)
1. Launch browser and and navigate to https://qa-ottoviz.ominf.net/
2. Log in with test credentials.
3. Selevt program "Camera System VI1"
4. Navigate to KPI Feature -> ISA -> Zone1
5. Sort the table by `False`.
6. Open first 7 DTIDs.
7. Count FN events.
8. Log the number of events per DTID into a report.
9. Close the browser.
