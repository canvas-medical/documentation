---
title: "Generate growth charts based on observations"
guide_for:
- /sdk/handlers/
- /sdk/events/
- /sdk/effects/
---

The [Growth charts Plugin](https://github.com/Medical-Software-Foundation/canvas/tree/main/extensions/growth-charts) was designed to help determine which percentile a patient falls into. We currently support both WHO and CDC growth charts, but it is possible to include additional charts if the same logic is applied

  - It uses the [`ACTION_BUTTON`](/sdk/handlers-action-buttons) handler to provide a button in the UI to launch the visualization.
  - We set `BUTTON_LOCATION = ActionButton.ButtonLocation.CHART_SUMMARY_VITALS_SECTION` to make the action button appear in the chart summary's vitals section 
  - Retrieves patient observations such as height, weight, BMI, and head circumference.
  - Uses a chart template to show the graphs
  - Predefined graph values are sourced from data files (e.g., who_boys_length_age), which can be included in the protocol.
  - Plots observations values onto the graphs
  - Uses the [`LAUNCH_MODAL`](/sdk/effects) effect to render a modal displaying the graphs results.

## Graphs structure

The graph data files have a simple structure, representing X and Y axes along with the resultant series:

To get the values to use on this plugin we used the following resources

[`World Health Organization (WHO)`](https://www.cdc.gov/growthcharts/who-data-files.htm)

[`Centers for Disease Control and Prevention (CDC)`](https://www.cdc.gov/growthcharts/cdc-growth-charts.htm)


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

## Getting patient data

For WHO and CDC growth charts, we need values like weight, length, BMI, etc. To obtain these, we use [`Observations`](/sdk/data-observation/).

```python
    patient = Patient.objects.get(id=self.target)
    sex_at_birth = patient.sex_at_birth
    birth_date = patient.birth_date

    observation_weight = Observation.objects.for_patient(self.target).filter(name="weight")
    observation_length = Observation.objects.for_patient(self.target).filter(name="length")
    observation_bmi = Observation.objects.for_patient(self.target).filter(name="bmi")
    observation_head_circumference = Observation.objects.for_patient(self.target).filter(name="head_circumference")
```

## Structure data to be used on graphs

With the patient’s values, we can then structure our data for plotting the graph

```python
    # value to be used on a particular graph
    weight_for_age = [
        x: "0", y: "10",
        x: "1", y: "12",
        x: "2", y: "14",
    ]

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
            "layerData": weight_for_age, # the patient’s data that will be plotted on the graph
            "tab": "WHO" # the section where the graph should be rendered (WHO or CDC)
        }
    ]
```

## Generate graphs and Launch Modal

To generate the graphs and [`LAUNCH_MODAL`](/sdk/effects) we use the chart template and pass the graphs as arguments.

```python
    launch_modal = LaunchModalEffect(
            content=render_to_string("templates/chart.html", {"graphs": graphs}),
        )
```

## The chart template and the result

This template is an HTML file (with CSS and JavaScript) that imports the [`D3js`](https://d3js.org/) library to help us generate the graphs.

It includes two sections (WHO and CDC), with options to convert the graph units (lbs/kg and cm/inches) and to print the current section.

The HTML file dynamically generates the graphs on the corresponding tab using the provided graph data and can be modified to include additional sections or support more units.

![vitals action button](/assets/images/vitals-action-button.png){: style='width: 300px'}

![chart template](/assets/images/growth-charts.png){: style='width: 600px'}
