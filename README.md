# MB_annotations_extractor

The goal is to create complete annotations in RDF for places and dates extracted from diary pages, along with a container that represents the event (time and place in which Mary Berenson was). The container should be structured as the datamodel: [img]
 
I thought of two different approaches:
1) asking llm to take a diary page, extract places mentioned in the text, and then create a correct RDF following a template passed in the prompt. Problems: incoherence of the results (sometimes correct UUID were generated, sometimes not) and incompleteness of the places extracted (it stopped at extracting only the place mentioned at the beginning of the diary). So asking directly could lead to inconsistent results in the direct production of the trig file. 

2) step-by-step approach extracting necessary values in JSON and then substituting those values into a standard trig file. In this case, the role of the LLM is to understand context, extract the place and link UUID, coordinates, wikidata entity to it, position in the paragraph. Other UUIDs are created afterwards using a library, as the correct date of creation. This ensures consistency and allows to extract more places, even those mentioned in the text. 

Same approach for dates. 

Creating an event is more difficult, because there's the need to combine both information contained in the previously generated trig and the text itself. The prompt has been structured to check the actual file and the related trigs, along with 5 following txt files (we assume that the files provided follow already a chronological order). The generated JSON contains UUIDs already generated when creating place and time trigs, a new UUID for the event, and a new UUID which represents and links this event to the following in chronological order (even if it's not contained in the same txt file). 

This process allows to have complete trig representing the annotations following OA schema and a container which sticks to the data model of the event. 

More on Wikidata reconciliation soon...

