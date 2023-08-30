---
title: "Template"
guide_for: 
 - /api/000-example-front-matter/
---

BLURB
<br>
<br> 

* * *
## What you'll learn
In this guide, you will learn how to do the following:
- section 1
- section 2
<br>
<br>

* * *


### Section 1
{% tabs XXX %}
{% tab XXX Developers %}
developer text
{% endtab %}
{% tab XXX Super Users %}
super user text
{% endtab %}
{% endtabs %}
<br>
* * *

### Section 2
{% tabs XXY %}
{% tab XXY Developers %}
developer text
{% endtab %}
{% tab XXY Super Users %}
super user text
{% endtab %}
{% endtabs %}


## Helpful Markdown / HTML 

## Link within docs
[text]({{site.baseurl}}/api/appointment/)

## External link
[text](https://canvas-medical.zendesk.com/hc/en-us/articles/4417495811859-Structured-Reason-for-Visit)

## Tabs
{% tabs XXY %}
{% tab XXY Developers %}
developer text
{% endtab %}
{% tab XXY Super Users %}
super user text
{% endtab %}
{% endtabs %}


## Adding Images


{:refdef: style="text-align: center;"}
![Protocol framework](/assets/images/alternative-med.png){:width="60%"}
{: refdef}

## Alert Samples

{% include alert.html type="success" content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque feugiat turpis id sollicitudin egestas. Etiam eu vestibulum magna, at gravida tellus. Sed rutrum est nec molestie bibendum." %}

{% include alert.html type="info" content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque feugiat turpis id sollicitudin egestas. Etiam eu vestibulum magna, at gravida tellus. Sed rutrum est nec molestie bibendum." %}

{% include alert.html type="warning" content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque feugiat turpis id sollicitudin egestas. Etiam eu vestibulum magna, at gravida tellus. Sed rutrum est nec molestie bibendum." %}

{% include alert.html type="danger" content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque feugiat turpis id sollicitudin egestas. Etiam eu vestibulum magna, at gravida tellus. Sed rutrum est nec molestie bibendum." %}
