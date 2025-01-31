---
title: "Surfacing data visualizations within the Canvas charting interface"
guide_for:
- /sdk/handlers/
- /sdk/events/
- /sdk/effects/
---

## Purpose

The Canvas SDK gives you access to real-time patient data and allows you to create custom UIs accessible from a patient’s chart. The combination of these capabilities allows you to create rich, interactive data visualizations your clinicians can access directly in the charting interface. This example will show you how we’ve used this approach to implement a pediatric growth charts feature.

## On this guide you will learn how to:

  - Use the [`ACTION_BUTTON`](/sdk/handlers-action-buttons) handler to provide a button, specify its location, and define its action in the UI.
  - Use the [`LAUNCH_MODAL`](/sdk/effects) effect to display a “Hello World” message.
  - Fetch patient observations, such as height and weight, from the [`SDK`](/sdk) and transform them for use in the charts.
  - Create an HTML template and pass in the patient data.
  - Use all of the above features to generate a Growth Chart and display it in the application.

## Growth Charts

Growth charts are percentile curves showing the distribution of selected body measurements in children. A growth chart shows how a child’s height, weight, and head circumference (for infants) compare to other children of the same age and sex. It helps track a child’s growth over time and can indicate whether they are growing at a healthy rate. Growth charts are commonly used by doctors to monitor development and identify potential health concerns.
On this guide we will use charts from the [`Center for Disease Control and Prevention (CDC)`](https://www.cdc.gov/growthcharts/who-data-files.htm) to demonstrate how you can create your own. 

## Our Plugin

Our complete plugin can be consulted on the [`Medical Software Foundation`](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/growth_charts/) and has 24 different types of growth charts. 

The plugin adds a button on the Vital Signs section of the patient chart that, when clicked, launches a modal displaying a generated HTML, which includes the height, weight, and head circumference measurements graphed against various percentile curves.

![vitals action button](/assets/images/vitals-action-button.png){: style='width: 300px'}

![chart template](/assets/images/growth-charts.png){: style='width: 600px'}

In the next steps, we will show you how we used the features above to create it.

## How to add a Button

To add a button to the vital signs section, you’ll implement an [`ACTION_BUTTON`](/sdk/handlers-action-buttons) handler. In your handler class, you’ll set the `BUTTON_LOCATION` constant to `ActionButton.ButtonLocation.CHART_SUMMARY_VITALS_SECTION` to make the action button appear in the corresponding section of the chart summary.

```python
    class GenerateVitalsGraphs(ActionButton):
        BUTTON_TITLE = "Growth Charts"
        BUTTON_KEY = "show_growth_charts"
        BUTTON_LOCATION = ActionButton.ButtonLocation.CHART_SUMMARY_VITALS_SECTION

     def handle(self) -> list[Effect]:
        # here we define what's the button action
```

## How to launch a modal on a button click

Now that you have your button showing in the chart section, you can launch a modal when it’s clicked using the [`LaunchModalEffect`](/sdk/layout-effect/#modals)

In this guide, we are launching a modal, although this click action can invoke any other plugin code

Here’s an example of a simple plugin using the Launch Modal effect to display an HTML “Hello World” message.

```python
    class HelloWorld(ActionButton):
        BUTTON_TITLE = "Hello World"
        BUTTON_KEY = "show_hello_world"
        BUTTON_LOCATION = ActionButton.ButtonLocation.
        
        def handle(self) -> list[Effect]:
            launch_modal = LaunchModalEffect(content=render_to_string("protocols/hello-world.html", { title: 'hello world' }))

    return [launch_modal.apply()]
```

And here's the result! 

![action button](/assets/images/action-button-hello-world.png){: style='width: 300px'}

![hello world](/assets/images/template-hello-world.png){: style='width: 400px'}


## How to fetch the observations

To retrieve the patient data we use the [`Data Module`](/sdk/data/) and more specifically, for this case, the [`Observation`](/sdk/data-observation/) model. 

Here, we get the `self.target`, which is the patient's `id`, to retrieve the patient and their observations by filtering for the values we need — such as weight, height, etc.

```python
    patient = Patient.objects.get(id=self.target)
    sex_at_birth = patient.sex_at_birth
    birth_date = patient.birth_date

    observation_weight = Observation.objects.for_patient(self.target).filter(name="weight")
    observation_length = Observation.objects.for_patient(self.target).filter(name="length")
    observation_bmi = Observation.objects.for_patient(self.target).filter(name="bmi")
    observation_head_circumference = Observation.objects.for_patient(self.target).filter(name="head_circumference")
```

## How to use html templates in the modal

The use of templates allows us to render any kind of information from the data we have. We can even import external libraries from CDNs and add CSS styles to customize and enhance our modal.

For example, to draw our graphs, we used d3js, a free, open-source JavaScript library for visualizing data. How to use d3js is outside the scope of this guide, but you can find great documentation and tutorials on the d3 site [`here`](https://d3js.org/getting-started)

Here's an example of a template file name `hello-world.html` that receives a variable called title, which will be used inside the template.

```html
<!DOCTYPE html>
<style>
    body {
        font-family: Arial, sans-serif;
        font-size: 30px;
    }
</style>
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
<html lang="en">
    <h1 id="main"></h1>
</html>
<script>
    const div = document.getElementById('main');
    div.textContent = `{{ title | safe }}`;
</script>
```

## How we render a growth chart in a template

To render a growth chart on the template, we first need to transform the Excel file we get from the CDC website into a JSON array and then pass it, along with the other necessary information, to the template (as we will see in the next step).

```python
    who_boys_length_age = [
        { "x": 0, "y": 46.77032, "z": "5th" },
        { "x": 1, "y": 51.52262, "z": "5th" },
        { "x": 2, "y": 55.13442, "z": "5th" },
        ...
        { "x": 23, "y": 92.93123, "z": "98th" },
        { "x": 24, "y": 93.92634, "z": "98th" }
    ]
```

## How do we use the patient data to plot the graph?

After obtaining the necessary information, we need to structure it in a way that can be used in the graph. To do this, we create a list of x and y values corresponding to the patient’s age and weight. With this list, we can add a line on top of the growth chart to compare both sets of data.

Here, we need to convert the weight since the Excel file has the values in kg, and our patient data is in lbs.

```python
     weight_for_age = {}

    for obs in observation_weight:
        if obs.value:
            note = Note.objects.get(dbid=obs.note_id)
            age_in_months = get_age_in_months(birth_date, note.datetime_of_service)
            weight_in_kg = convert_oz_to_kg(obs.value)
            weight_for_age[age_in_months] = weight_in_kg

     length_for_age = [
        { x: "0", y: "46" },
        { x: "1", y: "50" },
        { x: "2", y: "54" },
        { x: "2", y: "57" },
    ]
```

Finally, we create a list of graphs with the necessary variables and data, which are passed to the template to generate the graph.

```python
    # list of graphs
    graphs = [
        {
            "data": who_boys_length_age, # the data from the graph file
            "title": 'Length for age (Boys 0 - 2 years)', # graph title
            "xType": 'Generic', # the type of x axis (Generic, Length, Weight) - We need this info to convert the values 
            "yType": 'Length', # the type of y axis (Generic, Length, Weight)
            "xLabel": 'Age', # label for the x axis
            "yLabel": 'Length', # label for the y axis
            "zLabel": 'Percentile', # label for the z axis
            "layerData": length_for_age, # the patient’s data that will be plotted on the graph
            "tab": "WHO" # the section where the graph should be rendered (WHO or CDC)
        }
    ]
```

## Conclusion

By combining action buttons with the data module and the launch modal effect, you can create unique visualizations to help contextualize patient data for your clinical users.

