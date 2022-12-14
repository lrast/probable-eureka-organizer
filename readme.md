# Basic visual file organizer

## To run it:
1. set environment variables:
```
export FLASK_APP=run
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_SECRET_KEY=[key]
export FLASK_DATABASE_URL=[url]
```
2. flask run


## organization scheme:
1. track a database of webpages and local resources
2. resources are organized by tagging them with topic labels
3. organization is done at the level of topics, for example by make subsets of topics


## to do:
Majory priorities:
1. Start populating the database
2. usability features for adding: relationship editing, metadata editing
3. usability features for viewing: too long of lists

### Short term:
- topic autofill
- improve input interface
    * local file dialog -- this is difficult because the browser is explicitly sandboxed to hide local file locations
    * pdf ingestion: title, authors, references
- importing from mendeley and session buddy records
    > important for populating the database
- topic and citation graph visualization
    - to start: a series of trees with each unique root
- table view for pages including title, authors, journal, year
- interface to relationships
- super topics

### Long term:
- improve URL origin testing
- searching
- API design:
    * GET page: can fetch related topics (todo)
    * modularize commenting api
- dockerize
- Far future: shareability, searchability of libraries
- topic and citation graph visualization
