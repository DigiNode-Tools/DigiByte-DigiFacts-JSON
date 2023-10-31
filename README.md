# DigiByte-DigiFacts-JSON
A JSON file containing DigiByte DigiFacts.

### About the DigiFacts

These DigiFacts were originally created by several members of the DigiByte community back in 2021. The originals can be found [here](https://github.com/DigiByte-Core/DigiFacts). Since then, they have been significantly revised and expanded over time into the versions available here.

### Usage

#### Static DigiFacts

For best results download and cache the raw JSON file available here: https://raw.githubusercontent.com/saltedlolly/DigiByte-DigiFacts-JSON/main/digifacts.json

You should then periodically update your local version of this file from this address to ensure you have the latest DigiFacts. How often you do this is up to you, but at most once per day should be more than enough.

Note: This will soon be replaced by the new live DigiFacts below.

#### Dynamic DigiFacts (Coming Soon)

Dynamic DigiFacts includes live data which is updated every few minutes.

Query the live JSON data here: https://digifacts.digibyte.help/

Please cache reults and do not update more than once every 15 minutes.

### Using Dynamic Data in the DigiFacts

If you wish to insert dyanmic data into a DigiFact, please edit the digifacts-live.json file and insert any of the following variables:

| Variable         | Example Content | Note                                                |
|------------------|-----------------|-----------------------------------------------------|
| $blocks_tot      | 18826496        | Displays the current number of DigiByte blocks.  |
| $blocks_tot_cs   | 18,826,496      | Displays the current number of DigiByte blocks, with comma seperator. | 
| $blocks_tot_mil  | 18              | Displays the current number of DigiByte blocks rounded to the nearest million. |
| $nodes_mn_total  | 315             | Displays the total number of DigiByte mainnet nodes. |
| $nodes_tn_total  | 315             | Displays the total number of DigiByte testnet nodes. |

These variable will be replaced by live data every few minutes.

### Contributions

Contributions to this project from the community are actively encouraged. If you notice DigiFacts that are out of date or erroneous, please fork the repo and make a PR.

If you have a DigiByte project that you wish to make the community aware of, please add a new DigiFact. Be careful to use neutral wording - no marketing or advertisng is permitted, though a single DigiFact to tell the community about your project and what it offers is permitted.

URLs should ideally be included in both the content text, and in the seperate URL field. Ideally you should include only one URL per DigiFact.

Important: If you wish to insert a line break in your DigiFact, please use: \n

### Disclaimer

These DigiFacts are provided by the DigiByte community for the DigiByte community. It is up to the community to ensure they are current and accurate. Please make a PR with any corrections.

Uers should always do their own due diligence before using any of the services or products mentioned in these DigiFacts. They are provided for information purposes - mentions are not endorcements.

### Projects

The following projects are known to use this JSON file:

- [DigiNode Tools](https://github.com/saltedlolly/diginode-tools) - DigiFacts are displayed in the DigiNode Dashboard

### Revisions

Several of these DigiFacts require periodic updates to remain accurate. This list is provided as a helpful checklist for anyone making changes:

- DigiFact # 1 - Update from 18 to 19 Million blocks, when it happens.
