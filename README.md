# CostSplit
A Python package for calculating income and expenditure for large parties.

## Installation
Pip install from page?

1. Clone repository
2. `cd` into respository
3 `python3 -m pip install .`

## YAML-based Running
```bash
python3 costsplit.from_config <name_of_config_file>.yml
```
### Example Configuration File
```yaml
Trip1:
  Attendees:
    - Ethan
    - Flora
    - Blanca
    - Steph
  Transactions:
    Fondue:
      Payees: 
        Type: real
        Ethan: 100
      Participants:
        Type: weights
        Ethan: 1
        Flora: 1
        Blanca: 1
        Steph: 1
    Cocktails:
      Payees:
        Type: real
        Flora: 100
      Participants:
        Type: weights
        Ethan: 2
        Blanca: 1
        Flora: 1
        Steph: 1
```
