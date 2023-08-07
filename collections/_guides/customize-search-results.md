---
title: "Customize Search Results"
guide_for:
---
### Customize Search Results
Canvas's search functions are typically used dozens of times in a single patient interaction. Navigating through the thousands of options within a dropdown can be a daunting task for a clinician. Keywords and quickpicks can help improve the experience, but their impact is often limited. Our plugins allow you to add your own complex logic to help surface the right options, with the right context, at the right time. We currently support altering our condition search results through the Plugins beta, and will continue to expand this offering throughout the platform. 

{% include alert.html type="info" content=" If you are interested in participating in our beta for Plugins, please reach out to product@canvasmedical.com." %}

{% tabs CSR %}
{% tab CSR Developers %}
If your super users identify a way to optimize the current condition search results for your care model, you can leverage a plugin to alter the results as desired.

After following the quickstart guide...

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

{% endtab %}
{% tab CSR  Super Users %}
The plugin can alter the search in the following ways
Append Tags
Update Order
Remove Options


{% endtab %}
{% endtabs %}
