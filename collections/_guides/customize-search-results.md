---
title: "Customize Search Results"
guide_for:
---
Canvas's search functions are typically used dozens of times in a single patient interaction. Navigating through the thousands of options within a dropdown can be a daunting task for a clinician. Keywords and quickpicks can help improve the experience, but their impact is often limited. Our plugins allow you to add your own complex logic to help surface the right options, with the right context, at the right time. We currently support altering our condition search results through the Plugins beta, and will continue to expand this offering throughout the platform. 

{% include alert.html type="info" content=" If you are interested in participating in our beta for Plugins, please reach out to product@canvasmedical.com." %}

## Customize Condition Search

{% tabs CSR %}
{% tab CSR Developers %}
If your super users identify a way to optimize the current condition search results for your care model, you can leverage a plugin to alter the results as desired. Check out the super user tab for some examples.

<b>Condition search</b> can be modified by intercepting one of two events: <b>PreSearch</b> and <b>PostSearch</b>.

Use <b>PreSearch</b> if you want to entirely bypass the built-in Canvas search function entirely, and supply your own results based on the user query. In this case, you need to add results to the pre search event. They need to be formatted properly so that the application can use them correctly. You can specify the order and add annotations if desired. This could be useful if your care model has a narrow diagnostic range. The example below replaces the Canvas condition search results with the six options listed.

{% include alert.html type="warning" content="If you are going to remove all the Canvas results as a matter of course, it is better to use PreSearch, to avoid the delay associated with calling the Canvas search function."%}

```python
from canvas_core import events, logging
from canvas_core.search.events import PreSearch
from canvas_core.search.results import CONDITION_SEARCH, Condition, SearchResult

logger = logging.get_logger(__name__)

@events.handle_event(PreSearch, origin=CONDITION_SEARCH)
def handle_condition_presearch(event: PreSearch[Condition]) -> None:
    """Override the condition search result to return recommended conditions"""

    logger.info("Event Interception for Conditions", query=event.query, usage=event.usage)

    if event.usage != 'command.diagnose':
        return

    logger.info("Pre-searching for diangose conditions", query=event.query, usage=event.usage)


    event.results = [
        SearchResult[Condition](
            icd10_code="F32A",
            icd10_text= "Depression, unspecified",
            preferred_snomed_term="Depression, unspecified"
        ),
        SearchResult[Condition](
            icd10_code='F419',
            icd10_text='Anxiety disorder, unspecified',
            preferred_snomed_term='Anxiety disorder, unspecified'
        ),
       SearchResult[Condition](
            icd10_code='F319',
            icd10_text='Bipolar disorder, unspecified',
            preferred_snomed_term='Bipolar disorder, unspecified'
        ),
        SearchResult[Condition](
            icd10_code="F0391",
            icd10_text= "Unspecified dementia with behavioral disturbance",
            preferred_snomed_term="Unspecified dementia with behavioral disturbance"
        ),
        SearchResult[Condition](
            icd10_code='F4311',
            icd10_text='Post-traumatic stress disorder, acute',
            preferred_snomed_term='Post-traumatic stress disorder, acute'
        ),
       SearchResult[Condition](
            icd10_code='F840',
            icd10_text='Autistic disorder',
            preferred_snomed_term='Autistic disorder'
        )
    ]

    logger.info("Finished results for condition search", query=event.query)
```

Use <b>PostSearch</b> if you want to start with the results from the built-in Canvas search function and work with those. You can add results, remove results, reorder results, or annotate results. The example below adds HCC weight information to the search results for the specfied ICD10 codes.  

```python
from canvas_core import events, logging
from canvas_core.search import events as search_events
from canvas_core.search import results

logger = logging.get_logger(__name__)

HCC_WEIGHTS: dict[str, str] = {
    "I110": "HCC 85, weight 0.42",
    "T8621": "HCC 186, weight 1.0",
    "T8622": "HCC 186, weight 1.0",
    "I501": "HCC 85, weight 0.42",
    "I5020": "HCC 85, weight 0.42",
    "I5021": "HCC 85, weight 0.42",
    "I5022": "HCC 85, weight 0.42",
    "I5023": "HCC 85, weight 0.42",
    "I5030": "HCC 85, weight 0.42",
    "I5031": "HCC 85, weight 0.42",
    "I5032": "HCC 85, weight 0.42",
    "I5033": "HCC 85, weight 0.42",
}


@events.handle_event(search_events.PreSearch)
def handle_search_pre_search(event: search_events.PreSearch) -> None:
    """Log a message before a search request is executed."""
    logger.debug("Handling pre-search event.", source=event.source, query=event.query)


@events.handle_event(search_events.PostSearch, origin=results.CONDITION_SEARCH)
def handle_search_condition_post_search(event: search_events.PostSearch[results.Condition]) -> None:
    """Annotate condition search results with HCC weights."""
    for condition in event.results:
        if condition.data.icd10_code in HCC_WEIGHTS:
            condition.add_annotation(HCC_WEIGHTS[condition.data.icd10_code])

    logger.debug(
        "Handling post-search event.",
        source=event.source,
        query=event.query,
        results=event.results,
    )
```
<br>







{% endtab %}
{% tab CSR  Super Users %}
Custom plugins can be used to alter the condition search in the following ways:
- Replace the results entirely
    - 
- Add Results
- Remove Results 
- Reorder Results
- Add Annotations to Result


{% endtab %}
{% endtabs %}
