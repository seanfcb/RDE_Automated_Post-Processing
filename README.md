# RDE Automated Post-Processing

## Script requirements
Clone the RDE_ShotSheets repository in the parent directory (i.e. both repositories should be in the same parent directory)
```
git clone https://github.com/seanfcb/RDE_ShotSheets.git
```

This repository uses the file ScopeChannels.csv from RDE_ShotSheets to check the definition of each channel and assign a pressure range for each sensor used in any given RDE test.

## General use of repository
- Save the shot data from the Rigol oscilloscopes in a csv with the following naming structure:
```
shot###scp<1 or 2>_raw.csv
```
where ### corresponds to the shot number and <1 or 2> corresponds to either 1 or 2, the identifier of the oscilloscope used.
- Place the raw, unmodified data file in the directory RawData
- Run the script using
```
python3 merge_scopes_plot.py
```
- When prompted, enter the shot number you want to post-process.
- The script will open one figure at a time, while saving them as SVGs in ShotPlots/

### Incomplete data saves
Occasionally, the oscilloscopes will fail to trigger. When this happens, it is still possible to post-process the data, however the merge_scopes_plot.py script will not work since it requires data from two oscilloscopes. To post-process data from a single scope, run the following command using scope 1 as an example:
```
python3 scope1dat.py ###
```
Here, ### is a system argument which corresponds to the shot number you want to post-process. A file corresponding to this shot will be saved in the directory PressureTime. Creating plots or further post-processing this file will need to be done manually.
