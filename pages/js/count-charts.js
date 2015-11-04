var data;

var colors = {
  "Citizen": "#0072bc",
  "Mwananchi": "#529ecf",

  "Guardian": "#9FCA3C",
  "Nipashe": "#c2de81",

  "Daily News": "#b02334",
  "Habarileo": "#ba5763",
}

var publicationColors = function (d, i) {
    return colors[d.key];
}

var createChart = function(term, counts) {
  var cid = term.toLowerCase() + "-chart";
  addChartContainer(cid);

  nv.addGraph(function() {
    var chart = nv.models.multiBarChart()
      .showControls(false);
    
    chart.stacked(true);

    chart.xAxis
      .tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });

    var formatter = d3.format('d');
    chart.yAxis
      .axisLabel('Count (' + term + ')')
      .tickFormat(function (d) { 
        if (d < 0) d = -d; // No negative labels
        return formatter(d);
    });

    chart.color(publicationColors);

    d3.select('#' + cid + ' svg')
      .datum(counts)
      .transition().duration(350)
      .call(chart);

    nv.utils.windowResize(chart.update);

    return chart;
  });
}

var addChartContainer = function(cid) {
  $( '<div id="' + cid + '" class="chart"><svg></svg></div>' ).appendTo( "body" );
}

var addElectionTicks = function() {
  d3.selectAll('.chart svg')
    .append("line")
    .attr("y1", 30)
    .attr("y2", 275)
    .attr("x1", 885.5)
    .attr("x2", 885.5)
    .attr( "stroke", "#ff8a00" )
    .attr( "stroke-width", "2" );
}

d3.json("./pages/data/counts.json", function(error, json) {
  if (error) return console.warn(error);
  data = json;

  $.each(data, function(term, counts) {
    createChart(term, counts);
  })
  addElectionTicks();
}); 