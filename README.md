# DigiByte DigiFacts - JSON Web Service
Provides DigiByte DigiFacts in JSON format. Supports multiple languages and dynamic data.

## About the DigiFacts

These DigiFacts were originally created by several members of the DigiByte community back in 2021. The originals can be found [here](https://github.com/DigiByte-Core/DigiFacts). Since then, they have been significantly revised and expanded over time.

These DigiFacts are currently being translated into multiple languages. Please help by making improvements or adding translations for other languages.

## Disclaimer

These DigiFacts are provided by the DigiByte community for the DigiByte community. It is up to the community to ensure they are current and accurate. Please make a PR with any corrections.

Uers should always do their own due diligence before using any of the services or products mentioned in these DigiFacts. They are provided for information purposes - mentions are not endorcements.

## Usage

For DigiFacts in English, use: https://digifacts.digibyte.help/

For additional languages, use https://digifacts.digibyte.help/?lang=xx (Replace xx with one of the two letter language codes below.)

For more help, visit: https://digifacts.digibyte.help/?help

**IMPORTANT: Several of the DigiFacts include dynamic data (see below) and must be updated periodically so that they remain accurate - once every 15 minutes should be sufficient. Please avoid making too many frequent requests to the server - cache reults locally and do not update more than once every 15 minutes.**

## Contributions

Contributions to this project from the community are actively encouraged. If you notice DigiFacts that are out of date or erroneous, please fork the repo and make a PR.

If you have a DigiByte project that you wish to make the community aware of, please add a new DigiFact. Be careful to use neutral wording - no marketing or advertisng is permitted, though a single DigiFact to tell the community about your project and what it offers is permitted.

URLs should be included both within the content text, and in the seperate URL field. This allows for easier processing. Please include only one URL per DigiFact.

### Using Dynamic Data in the DigiFacts

If you wish to insert dynamic data into a DigiFact, please edit the digifacts.json file and insert any of the following variables:

| Variable               | Example Content | Note                                                |
|------------------------|-----------------|-----------------------------------------------------|
| ```$blocks_tot```      | 18826496        | Displays the current number of DigiByte blocks.  |
| ```$blocks_tot_cs```   | 18,826,496      | Displays the current number of DigiByte blocks, with comma seperator. | 
| ```$blocks_tot_mil```  | 18              | Displays the current number of DigiByte blocks rounded to the nearest million. |
| ```$nodes_mn_total```  | 315             | Displays the total number of DigiByte mainnet nodes. |
| ```$nodes_tn_total```  | 315             | Displays the total number of DigiByte testnet nodes. |

These variable will be replaced by live data every few minutes.

### Translations

Translations should be based on the English version of each DigiFact. New DigiFacts must be added in English first with other languages beneath it.

Please help by providing translations for additional langauges, or improving existing ones. Please update the table below when you make changes, including a link to your Github profile.

To get started, please fork the repo. Edit digifacts.json and make a PR with your changes. Please check the JSON is valid before doing do.

| Language                 | Verified by                                      | Last Updated | Status                                              |
|--------------------------|--------------------------------------------------|--------------|-----------------------------------------------------|
| en English               | [@saltedlolly](https://github.com/saltedlolly)   | 2023-11-01   |                                                     |
| zh Chinese (Simplified)  |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| ru Russian               |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| es Spanish               |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| ko Korean                |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| ja Japanese              |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| de German                |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| fr French                |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| pt Portuguese            |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| hi Hindi.                |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| nl Dutch.                |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 

## Projects

The following projects are known to use this service:

- [DigiNode Tools](https://github.com/saltedlolly/diginode-tools) - DigiFacts are displayed in the DigiNode Dashboard

