# DigiByte DigiFacts - JSON Web Service
Provides DigiByte DigiFacts in JSON format. Supports multiple languages and dynamic data.

## About DigiByte DigiFacts

The DigiFacts were originally created by several members of the DigiByte community back in 2021. The originals can be found [here](https://github.com/DigiByte-Core/DigiFacts). Since then, they have been significantly revised and expanded over time.

By providing them in JSON format, it is now easy for developers to use them in their projects to help educate their users about DigiByte. They are also now in a format that makes them easy to be updated and expanded in the future.

## Disclaimer

These DigiFacts are provided by the DigiByte community for the DigiByte community. It is up to the community to ensure they are current and accurate. Please make a PR with any corrections.

Users should always do their own due diligence before using any of the services or products mentioned in these DigiFacts. They are provided for information purposes - mentions are not endorcements.

## Usage

The DigiFacts are currently available in 12 languages listed below. It is suggested that developers query these feeds once every 15 mintues.

**IMPORTANT: Several of the DigiFacts include dynamic data (see below) and must be updated periodically so that they remain accurate - querying the server once every 15 minutes per language should be sufficient. Please do not exceed this by making frequent requests to the server.**

| Language               | JSON URL                                             | Proofreading Links
|------------------------|------------------------------------------------------|----------------------------------------------------|
| English                | https://digifacts.digibyte.help/                     | <a href="https://digifacts.digibyte.help/?proofread">Proofread English</a>       |
| Chinese (Simplified)   | https://digifacts.digibyte.help/?lang=zh              | <a href="https://digifacts.digibyte.help/?lang=zh&proofread">Proofread Chinese (Simplified)</a>       |
| Russian                | https://digifacts.digibyte.help/?lang=ru              | <a href="https://digifacts.digibyte.help/?lang=ru&proofread">Proofread Russian</a>       |
| Spanish                | https://digifacts.digibyte.help/?lang=es              | <a href="https://digifacts.digibyte.help/?lang=es&proofread">Proofread Spanish</a>       |
| Korean                 | https://digifacts.digibyte.help/?lang=ko              | <a href="https://digifacts.digibyte.help/?lang=ko&proofread">Proofread Korean</a>       |
| Japanese               | https://digifacts.digibyte.help/?lang=ja              | <a href="https://digifacts.digibyte.help/?lang=ja&proofread">Proofread Japanese</a>       |
| German                 | https://digifacts.digibyte.help/?lang=de              | <a href="https://digifacts.digibyte.help/?lang=de&proofread">Proofread German</a>       |
| French                 | https://digifacts.digibyte.help/?lang=fr              | <a href="https://digifacts.digibyte.help/?lang=fr&proofread">Proofread French</a>       |
| Portuguese             | https://digifacts.digibyte.help/?lang=pt              | <a href="https://digifacts.digibyte.help/?lang=pt&proofread">Proofread Portuguese</a>       |
| Hindi                  | https://digifacts.digibyte.help/?lang=hi              | <a href="https://digifacts.digibyte.help/?lang=hi&proofread">Proofread Hindi</a>       |
| Dutch                  | https://digifacts.digibyte.help/?lang=nl              | <a href="https://digifacts.digibyte.help/?lang=nl&proofread">Proofread Dutch</a>       |
| Italian                | https://digifacts.digibyte.help/?lang=it              | <a href="https://digifacts.digibyte.help/?lang=it&proofread">Proofread Italian</a>       | 

For more help, visit: https://digifacts.digibyte.help/?help

## Contributions

Contributions to this project from the community are actively encouraged. If you notice DigiFacts that are out of date or erroneous, please fork the repo and make a PR. You can also create an Issue [here](https://github.com/saltedlolly/DigiByte-DigiFacts-JSON/issues). 

### Translations

We need volunteer native speakers to take responsibility for each language, translating and proofreading when needed. If you can help, please join the ["DigiFact Translation Team" Telegram group](https://t.me/DigiByteDigiFacts).

Support for the initial 12 languages was added with help from ChatGPT. For this reason, they all need proofreading by a native speaker. Please help if you can. To make this easier you can use the proofreading links above, which display the English DigiFacts alongside their translation, formatted so that they are easy to read. To submit improvements, please fork the repo, edit the digifacts-multilang.json file, and make a PR with your changes. Please check the JSON is valid before doing do.

If you are interested in helping translate the DigiFacts into additional languages, you can find a step-by-step Translation Guide [here](translation-guide.md) for how to do this with help from ChatGPT.

If you contribute a new language, or are willing to take responibility for an existing one, please add your Github handle to the table below.

| Language                 | Last Verified by                                 | Last Updated | Status                                              |
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
| hi Hindi                 |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| nl Dutch                 |                                                  | 2023-11-01   | Needs checking - currently chatGPT translation      | 
| it Italian               |                                                  | 2023-11-03   | Needs checking - currently chatGPT translation      |

### Adding new DigiFacts

Everybody is encouraged to help contribute new DigiFacts. If you have a DigiByte project that you wish to make the community aware of, please add a new DigiFact. Be careful to use neutral wording - no marketing or advertisng is permitted, though a single DigiFact to tell the community about your project and what it does is permitted.

Important considerations:
- New DigiFacts must be added in English first. This will then be used as the basis for the translation into other languages.
- URLs should be included both within the content text, and in the seperate URL field. This allows for easier processing. Please include only one URL per DigiFact.
- Please avoid creating DigiFacts about price - DigiFacts are for educating the community about DigiByte only.

### Using Dynamic Data in the DigiFacts

If you wish to insert dynamic data into a DigiFact, please edit the digifacts-multilang.json file and insert any of the following variables:

| Variable               | Example Content | Note                                                |
|------------------------|-----------------|-----------------------------------------------------|
| ```$blocks_tot```      | 18826496        | Displays the current number of DigiByte blocks.  |
| ```$blocks_tot_cs```   | 18,826,496      | Displays the current number of DigiByte blocks, with comma seperator. | 
| ```$blocks_tot_mil```  | 18              | Displays the current number of DigiByte blocks rounded to the nearest million. |
| ```$nodes_mn_total```  | 315             | Displays the total number of DigiByte mainnet nodes. |
| ```$nodes_tn_total```  | 315             | Displays the total number of DigiByte testnet nodes. |

These variable will be replaced by live data every few minutes.

## Projects

The following projects are known to use this service:

- [DigiNode Tools](https://github.com/saltedlolly/diginode-tools) - DigiFacts are displayed in the DigiNode Dashboard

