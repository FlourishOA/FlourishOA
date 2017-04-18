/**
 * Created by pspieker on 4/17/17.
 */

var margin = {top: 20, right: 50, bottom: 250, left: 45},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var x = d3.scaleBand()
    .rangeRound([0, width], .1)
	.paddingInner(0.1);

var y = d3.scaleLinear()
    .range([height, 0]);

var xAxis = d3.axisBottom()
    .scale(x)
    .tickPadding(10);

var yAxis = d3.axisLeft()
    .scale(y)
    .ticks(10)
    .tickFormat( function(d) { return "$" + d } ); // Add dollar sign to y axis

tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .direction('n');

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .call(tip)
    .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


var dataset; //the full dataset

// Assign timeParse & timeFormat function to a variable for later use
var parseDate = d3.timeParse("%Y-%m-%d");
var formatDate = d3.timeFormat("%m-%d-%Y")

d3.csv("./static/view2_data.csv", function(error, data) {
//read in the data stored in same folder
	if (error) return console.warn(error);
	data.forEach(function(d) {  // assign data types to each column
		d.price = +d.price;
		d.date_stamp1 = parseDate(d.date_stamp1);
		d.category = (d.category);
	});

// Define what happens when drop down menu option is selected
$("#myselectform").change(function() {
				var yearFinder = $("#myselectform").find(":selected").text();
				filterType(yearFinder);
				})

// dataset is the full dataset -- maintain a copy of this at all times
dataset = data;

// Draw the visualization as per function
drawVis(dataset);

// Define the drawVis function
function drawVis(dataset) {
    // Create new array with key value categories and mean price per category
    var pricesAvgAmount = d3.nest()
    .key(function(d) { return d.category; })
    .rollup(function(v) { return d3.mean(v, function(d) { return d.price; }); })
    .entries(dataset);

    // Sort the data by the category name alphabetically
    pricesAvgAmount = pricesAvgAmount.sort(function (a,b) {return d3.ascending(a.key, b.key);});

    // Set the domains of the x and y axes
    x.domain(pricesAvgAmount.map(function(d) { return d.key; }));
    y.domain([0, Math.ceil(d3.max(pricesAvgAmount, function(d) { return d.value; })/ 1000.0)*1000]); // the domain value of y is 0 to the max y value rounded up to the nearest thousand

    var ChartGroup = svg.append("g") // this element will bind the axes and the charts
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Append x axis
    ChartGroup.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")") // shifts the axis from the top of the svg object to the bottom
        .call(xAxis)
        .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-.8em")
            .attr("dy", "-.5em")
            .attr("transform", "rotate(-65)"); // rotate axis labels

    // Append an x-axis label
    ChartGroup.append("text")
            .attr("y", 420)
            .attr("x", width/2)
            .attr("dy", "1em")
            .style("text-anchor", "end")
            .text("Journal Category")

    // Append a y-axis label
    ChartGroup.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", -65)
            .attr("x", -10)
            .attr("dy", "1em")
            .style("text-anchor", "end")
            .text("Average Article Processing Charge");

    // Append the y axis
    ChartGroup.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    // Link data to bars
    ChartGroup.selectAll(".bar")
        .data(pricesAvgAmount)
        .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.key); })
            .attr("width", x.bandwidth())
            .attr("y", function(d) { return y(d.value); })
            .attr("height", function(d) { return height - y(d.value); })
            .on("mouseover", function(d) {
                    tip
                        .html(function() {
                            return d.key + ": $" + d.value.toFixed(2)
                        })
                        .show()
                    ;
                })
            .on("mouseout", tip.hide);



    // Set the checkbox to unchecked
    document.getElementById("check").checked = false;

    // When checkbox status is changed, run change function
    d3.select("input").on("change", change);

    // Define what should happen when check box is checked
    function change() {

        var x0 = x.domain(pricesAvgAmount.sort(this.checked
            ? function(a, b) { return b.value - a.value; }
            : function(a, b) { return d3.ascending(a.key, b.key); })
            .map(function(d) { return d.key; }))
            .copy();

        svg.selectAll(".bar")
            .sort(function(a, b) { return x0(a.key) - x0(b.key); });

        var transition = svg.transition().duration(750),
        delay = function(d, i) { return i * 50; };

        transition.selectAll(".bar")
            .delay(delay)
            .attr("x", function(d) { return x0(d.key); });

        transition.select(".x.axis")
            .call(xAxis)
        .selectAll("g");
    }
}
// Redraw vis if drop-down menu is used
function filterType(mtype) {
	var patt = new RegExp("all");
	var res = patt.test(mtype.toLowerCase());
		if(res){
            svg.selectAll("*").remove();
			drawVis(dataset);
		} else {
            svg.selectAll("*").remove();
			var ndata = data.filter(function(d) {
				console.log(mtype)
		    return String(formatDate(d.date_stamp1).split("-")[2]) == mtype;
		    });
	        drawVis(ndata);
		}
}

});

