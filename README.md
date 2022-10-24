# Seating Plan Tool
Tool to write assign seats at Vlerick Bussines school.
## Use
```console
python assignSeats.py
```
Will display seating plan image and saves seating plan as pdf and png.
## Data requirements
A data directory is required to run it but has been ommited for privacy reasons.
data dir needs following layout.
```
data
│   people.csv    
└──photos
    | lastname firstname.jpg
```
people.csv contains data about everybody needing assingment and must contain following columns:
* firstName
* LastName
* badSeats: how often this person has been assigned a bad seat in the past.