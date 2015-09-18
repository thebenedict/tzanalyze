var data = {}

var colors = {
  "Citizen": "#0072bc",
  "Mwananchi": "#529ecf",

  "Guardian": "#9FCA3C",
  "Nipashe": "#c2de81",

  "Daily News": "#b02334",
  "Habarileo": "#ba5763",
}

var getData = function (term) { return data[term]; }

var publicationColors = function (d, i) {
    return colors[d.key];
}

d3.json("./pages/data/ccm.json", function(error, json) {
  if (error) return console.warn(error);
  data['ccm'] = json;

  nv.addGraph(function() {
    var chart = nv.models.multiBarChart()
      .showControls(false);
    
      chart.stacked(true);

      chart.xAxis
        .tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });

      var formatter = d3.format('d');
      chart.yAxis
        .axisLabel('Count (CCM)')
        .tickFormat(function (d) { 
          if (d < 0) d = -d; // No nagative labels
          return formatter(d);
      });

      chart.color(publicationColors);

      d3.select('#ccm-chart svg')
        .datum(getData('ccm'))
        .transition().duration(350)
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
  });
});

d3.json("./pages/data/chadema.json", function(error, json) {
  if (error) return console.warn(error);
  data['chadema'] = json;
  nv.addGraph(function() {
    var chart = nv.models.multiBarChart()
      .showControls(false);
    
      chart.stacked(true);

      chart.xAxis
        .tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });

      var formatter = d3.format('d');
      chart.yAxis
        .axisLabel('Count (CHADEMA)')
        .tickFormat(function (d) { 
          if (d < 0) d = -d; // No nagative labels
          return formatter(d);
      });

      chart.color(publicationColors);

      d3.select('#chadema-chart svg')
        .datum(getData('chadema'))
        .transition().duration(350)
        .call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
  });
});