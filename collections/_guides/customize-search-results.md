---
title: "Customize Search Results"
last_modified_at: "2026-05-30"
guide_for:
- /sdk/events/
- /sdk/effects/
- /sdk/protocols/
- /sdk/handlers/
---
In a typical visit note, it's common for clinicians to make 20, 30, even 50 or more selections from structured terminologies with commands like Diagnose, Prescribe, Family History, and many more. You can help clinicians make faster and more accurate selections with Canvas plugins. Write simple plugin code to apply custom filtering, sorting, and search result annotations in real time with near zero latency.

This search modification can help clinicians:

- Choose the most appropriate medication that is also covered by insurance
- Prioritize in-network specialists
- Consider appropriate risk adjustment factors when selecting diagnosis codes

Canvas supports modifying search results in [all refactored commands](/product-updates/commands-module/#progress).


First, we'll show you a complete example of customizing the search results for
choosing a medication in a Medication Statement command, then we'll break it
down piece by piece so you can adapt the example to your own needs.

## The Complete Example

This example checks for the presence of a particular medication in the search
results and, if present, annotates that medication option with additional
information and adjusts its position to the top of the search results.

For reference, here's the difference in behavior with the plugin inactive vs
active:

**Inactive (normal behavior):**

![With the plugin inactive, the results are unaltered](/assets/images/customize-search-results/plugin-inactive.png){: style='width: 400px'}

**Active (modified behavior):**

![With the plugin active, the preferred result is listed first, and with additional context](/assets/images/customize-search-results/plugin-active.png){: style='width: 400px'}


Here's the code in its entirety:

```python
import json

from canvas_sdk.events import EventType
from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.handlers import BaseHandler


class Handler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.MEDICATION_STATEMENT__MEDICATION__POST_SEARCH)

    def compute(self):
        results = self.context.get("results")

        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]

        post_processed_results = []
        for result in results:
            should_float_to_top = False
            for coding in result.get("extra", {}).get("coding", []):
                if (
                    coding.get("code") == 554704
                    and coding.get("system") == "http://www.fdbhealth.com/"
                ):
                    if result.get("annotations") is None:
                        result["annotations"] = []
                    result["annotations"].append("Kirkland Signature")
                    should_float_to_top = True
            if should_float_to_top:
                post_processed_results.insert(0, result)
            else:
                post_processed_results.append(result)

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

## Anatomy of the Example

This code can be broken down into the following sections:
- Register interest in the correct search event
- Decide whether to make any changes
- Loop through the results, making modifications as appropriate
- Return the modified results as a properly typed effect

### Register interest in the correct search event

```python
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler


class Handler(BaseHandler):
    RESPONDS_TO = EventType.Name(EventType.MEDICATION_STATEMENT__MEDICATION__POST_SEARCH)

    def compute(self):
        results = self.context.get("results")
```

The class inherits from `BaseHandler`, which clues the plugin-runner into
registering your code as interested in the event or events listed in the
`RESPONDS_TO` class constant. We only specify one event here,
`MEDICATION_STATEMENT__MEDICATION__POST_SEARCH`, but you could make this value
a list to fire on multiple events. The event we've chosen to listen for can be
read backwards to understand when it fires. This event is emitted after ("_post_") the
normal _search_ results are found for the _medication_ autocomplete field of the
_medication statement_ command. This event comes with a context that contains the
search results that would be served to the user if there were no
modifications.

### Decide whether to make any changes

```python?partial=true
        if results is None:
            return [Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))]
```

If the value of the results `is None`, we bail out early. There is a subtle
difference between results of `None` and an empty result set (`[]`). Results
being `None` means "make no changes, present the results without modification",
whereas an empty result set means "present no options to the user".

### Loop through the results, making modifications as appropriate

```python?partial=true
        post_processed_results = []
        for result in results:
            should_float_to_top = False
            for coding in result.get("extra", {}).get("coding", []):
                if (
                    coding.get("code") == 554704
                    and coding.get("system") == "http://www.fdbhealth.com/"
                ):
                    if result.get("annotations") is None:
                        result["annotations"] = []
                    result["annotations"].append("Kirkland Signature")
                    should_float_to_top = True
            if should_float_to_top:
                post_processed_results.insert(0, result)
            else:
                post_processed_results.append(result)
```

In this block of code, we create a new list named `post_processed_results` to
hold our modified result set. We then loop through each result in the
unmodified results set, and check to see if the current medication result matches our
chosen criteria (FDB code 554704).

If it does match, we first check to see if any
annotations already exist and initialize the annotations list if needed. We
then append our chosen annotation to the result's annotation list and flag it
as needing to be floated to the top (we had defaulted it to not be floated
earlier on).

Finally, we add the result to our parallel list, `post_processed_results`. If
it matched and was marked as being floated to the top, we insert it into the
list at position 0. If it did not match, we append the result to the end of
the list.

### Return the modified results as a properly typed effect

```python?partial=true
        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(post_processed_results),
            )
        ]
```

With our list of modified results in place, we just need to return an effect
of type `AUTOCOMPLETE_SEARCH_RESULTS` with our modified list as the payload.

The dropdown of options presented to the user now reflects our modifications!

## Understanding Search Result Data Structures

The search results in this example follow the MedicationSearchResult structure. Each result contains fields like `text`, `disabled`, `description`, `annotations`, `extra`, and `value` that provide detailed information about the medication option.

For complete details about medication search result data contracts and other search result structures, see the [Search Result Data Structures](/sdk/events/#search-result-data-structures) section in the Events documentation.

## Offering your own providers alongside the directory

The four provider-search surfaces — Refer, Imaging Order, fax recipient, and a patient's external
care team — search the shared contact directory by default. Providers you create with the
[ServiceProvider effect](/sdk/effect-service-provider/) are not searched automatically, so if you
maintain your own directory you have to offer them yourself.

The pattern is the same on all four surfaces: query your own
[ServiceProvider](/sdk/data-serviceprovider/) records, put them ahead of the directory's results, and
return the combined list.

**Use the POST_SEARCH event, not PRE_SEARCH.** Only the post-search context carries what the
directory returned, in `context["results"]`. On a pre-search that list is empty, so there is nothing
to merge with — and on a command pre-search any `AUTOCOMPLETE_SEARCH_RESULTS` effect you return is
authoritative, which means an empty reply blanks the dropdown instead of leaving it alone.

Which helper you call depends on the surface:

| Surface | Event | Helper |
| --- | --- | --- |
| Refer | `REFER__REFER_TO__POST_SEARCH` | `as_search_result()` |
| Imaging Order | `IMAGING_ORDER__IMAGING_CENTER__POST_SEARCH` | `as_search_result()` |
| Fax recipient | `FAX__RECIPIENT__POST_SEARCH` | `as_search_contact()` |
| External care team | `PATIENT_PROFILE__EXTERNAL_CARE_TEAM__POST_SEARCH` | `as_search_contact()` |

```python
import json

from canvas_sdk.effects import Effect, EffectType
from canvas_sdk.events import EventType
from canvas_sdk.handlers import BaseHandler
from canvas_sdk.v1.data import ServiceProvider

# Cap the query so a loose search term cannot pull your whole table into the sandbox.
MAX_LOCAL_PROVIDERS = 200

# The sandbox has no Q objects, so each field is queried separately and unioned in Python.
SEARCHABLE_FIELDS = ("first_name", "last_name", "practice_name", "specialty")


def matching_providers(search_term):
    matches = {}
    for field in SEARCHABLE_FIELDS:
        providers = ServiceProvider.objects.filter(
            is_active=True, **{f"{field}__icontains": search_term}
        )[:MAX_LOCAL_PROVIDERS]
        for provider in providers:
            matches.setdefault(provider.dbid, provider)

    return list(matches.values())[:MAX_LOCAL_PROVIDERS]


class ContactDirectorySearch(BaseHandler):
    """Offer our own providers above the directory's on the fax and care team searches."""

    RESPONDS_TO = [
        EventType.Name(EventType.FAX__RECIPIENT__POST_SEARCH),
        EventType.Name(EventType.PATIENT_PROFILE__EXTERNAL_CARE_TEAM__POST_SEARCH),
    ]

    def compute(self):
        search_term = str(self.event.context.get("search_term") or "").strip()
        if not search_term:
            # An empty term must not push the entire local directory into the dropdown.
            return self.no_opinion()

        matches = matching_providers(search_term)
        if not matches:
            return self.no_opinion()

        ours = [
            provider.as_search_contact(["Our directory"])
            for provider in matches
        ]

        # Keep the directory's results underneath, minus anyone we already offered.
        superseded = {provider.full_name.lower() for provider in matches}
        theirs = [
            result
            for result in (self.event.context.get("results") or [])
            if f"{result.get('firstName') or ''} {result.get('lastName') or ''}".strip().lower()
            not in superseded
        ]

        return [
            Effect(
                type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS,
                payload=json.dumps(ours + theirs),
            )
        ]

    def no_opinion(self):
        """A null payload means "keep whatever the search already found"."""
        return [
            Effect(type=EffectType.AUTOCOMPLETE_SEARCH_RESULTS, payload=json.dumps(None))
        ]
```

For Refer and Imaging Order, subscribe to those two events instead and swap `as_search_contact()` for
`as_search_result()`. The merge is the same, except the directory's results carry their display name
in `text` rather than in `firstName` / `lastName`.

A few things worth carrying over into your own version:

- **Filter to `is_active=True`.** Deactivating a provider is how a customer retires it, so offering a
  deactivated one invites picking it again.
- **Return a null payload when you have nothing to add**, rather than an empty list. On the contact
  surfaces an empty list clears the results.
- **Prefer your own record when it duplicates a directory contact.** Selecting your record threads
  its `service_provider_id` through to the commit, so the existing row is reused instead of a
  near-duplicate being written. Match conservatively — listing a provider twice is a smaller failure
  than hiding one.
- **Annotate what you add** so the user can tell your entries from the directory's.

## Accessing User Context

PRE_SEARCH and POST_SEARCH events include information about the user performing the search in the event context. This includes search events for command fields like prescriber, medication, diagnosis, pharmacy, and many others. It also includes the non-command fax recipient and external care team directory searches listed under [Other Events](/sdk/events/#other-events). All of these searches can be customized the same way.

You can access the user's staff key from the context:

```python
def compute(self):
    user_context = self.context.get("user", {})
    staff_key = user_context.get("staff")

    # Use the staff key to customize search results
    # based on the user's role, preferences, or permissions
```

This can be useful for customizing search results based on:
- User-specific preferences or settings
- Role-based filtering (e.g., showing different prescriber options based on the user's specialty)
- Permission-based access control
- User's organization or practice location

## Mapping Lay Terms to Medical Terms

<!-- sources: discussion #935 -->
<!-- REVIEW: clinical-accuracy sign-off required -->

A common question is whether custom search results can map an over-general lay term to a proper medical term and coding — for example, surfacing *Essential hypertension (I10)* when a clinician searches for "high blood pressure."

What these events give you is the ability to **modify the result set that Canvas returns for a search**. In a `POST_SEARCH` handler you receive the results Canvas found for the user's query in `self.context["results"]`, and you can reorder them, annotate them, filter them, or add to them before they are shown — exactly as the example above floats a preferred medication to the top. So if a search for a lay term already returns the medical concept you want among its results, you can promote and annotate that result so the clinician sees it first.

The search events are not a free-text translation layer, however: the events carry the structured search results rather than an arbitrary mapping from any phrase to any coding. If you need to act on the exact text the user typed (to recognize specific lay phrases), inspect the search context the event provides rather than relying on the rendered UI. Because terminology mapping touches clinical coding accuracy, validate any term-to-code associations with your clinical team before deploying.

## Watch Me Build It

<div style="position: relative; padding-bottom: 56.25%; height: 0;"><iframe src="https://www.loom.com/embed/d3b696bdb482401c82aad2a2347c11ea?sid=07417cab-cb22-4165-ba16-2a2dcc2b3ce5" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div> 

<br />
<br />
<br />
