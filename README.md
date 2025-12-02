# SpecFit: a graphical interface for plasma characterization

## Custom databases
To add a new database, create a folder with the following layout:

    └─── custom_database
        ├── database
        │   ├── rad_001_001.txt
        │   ├── rad_001_002.txt
        │   └── ...
        ├── lineout
        │   ├── sample1.txt
        │   ├── sample2.txt
        │   └── ...
        ├── database.py
        ├── database.toml
        ├── tab_clength.txt
        ├── tab_dne.txt
        └── tab_tev.txt

The subfolders `database` and `lineout` contain synthetic spectra files and experimental samples, respectively. Tables for the conditions of characteristic length, electron density and electron temperature are stored in `tab_clength.txt`, `tab_dne.txt`and `tab_tev.txt`.

The file `database.py` acts as an optional python module to store additional case-dependent funcionality.