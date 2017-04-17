// Assign timeParse function to a variable for later use
var parseDate = d3.timeParse("%Y-%m-%d");
var formatDate = d3.timeFormat("%Y-%m-%d");

    
// Define heights, widths, margins
var width = 950;
var height = 550;
var margin = {top: 30, right: 30, bottom: 80, left: 40};
    var w = width - margin.left - margin.right;
    var h = height - margin.top - margin.bottom;

var dataset; //the full dataset

d3.csv("../../static/ScatterplotViz/clean_data.csv", function(error, data) {
//read in the data stored in same folder
	if (error) return console.warn(error);
	data.forEach(function(d) {  // assign data types to each column
		d.price = +d.price;
		d.date_stamp1 = parseDate(d.date_stamp1);
		d.date_stamp2 = parseDate(d.date_stamp2);
		d.journal_id = String(d.journal_id);
		d.article_influence = +d.article_influence;
		d.journal_name = String(d.journal_name);
		d.category = String(d.category);
	});


//dataset is the full dataset -- maintain a copy of this at all times
dataset = data;

//all the data is now loaded, so draw the initial vis
  drawVis(dataset);

});

// Define color variable
var col = d3.scaleOrdinal(d3.schemeCategory20);


var svg = d3.select("#sp-viz").append("svg")
    .attr("width", w + margin.left + margin.right)
    .attr("height", h + margin.top + margin.bottom)
  .append("g") 
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// gridlines in x axis function
function make_x_gridlines() {		
    return d3.axisBottom(x)
        .ticks(10)
}

// gridlines in y axis function
function make_y_gridlines() {		
    return d3.axisLeft(y)
        .ticks(10)
}

// add the variable tooltip set to invisible
var tooltip = d3.select("#sp-viz")
		.append("div")
    	.attr("class", "tooltip")
    	.style("opacity", 0);


var x = d3.scaleLinear(x)
	.domain([0, 4000]) // domain value determined by x max value
	.range([0, w]);
	
	
var y = d3.scaleLinear(y)
	.domain([0, 10]) // domain value determined by y max value
	.range([h, 0]); // format of height, 0 allows y-axis to grow from bottom up

// add the X gridlines
  svg.append("g")			
      .attr("class", "grid")
      .attr("transform", "translate(0," + h + ")")
      .call(make_x_gridlines()
          .tickSize(-h)
          .tickFormat("")
      )

  // add the Y gridlines
  svg.append("g")			
      .attr("class", "grid")
      .call(make_y_gridlines()
          .tickSize(-w)
          .tickFormat("")
      )


var xAxis = d3.axisBottom() // axisBottom refers to where to put the labels relative to the line. 
	.ticks(7) // number of ticks
	.tickPadding(8) // add space between ticks and labels
	.tickSize(10) // increase the length of the ticks
	.scale(x)
	.tickFormat( function(d) { return "$" + d } ); // Add dollar sign to x axis;

svg.append("g")
		.attr("transform", "translate(0," + h + ")") // shifts the axis from the top of the svg object to the bottom
		.attr("class", "axis x") // add a class element
		.call(xAxis);


svg.append("text")
        .attr("y", 490)
        .attr("x", w / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Article Processing Charge");
	
	
var yAxis = d3.axisLeft() // axisLeft refers to where to put the labels relative to the line
	.ticks(10) // number of ticks
	.tickPadding(5) // add space between ticks and labels
	.tickSize(5) // increase the length of the ticks
	.scale(y);
	
svg.append("g")
	.attr("class", "axis y") //add a class element
	.call(yAxis);
	
svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -(h / 2))
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .text("Article Influence Score");


d3.selection.prototype.moveToBack = function() { 
    return this.each(function() { 
        var firstChild = this.parentNode.firstChild; 
        if (firstChild) { 
            this.parentNode.insertBefore(this, firstChild); 
        } 
    }); 
}; 

function drawVis(dataset) { //draw the circles initially and on each interaction with a control

	var circle = svg.selectAll("circle")
		.data(dataset); 
	

	circle
    	  .attr("cx", function(d) { return x(d.price);  }) // x value based on price
    	  .attr("cy", function(d) { return y(d.article_influence);  }) // y value based on article_influence
		  .style("stroke-width", 2)
		  .style("stroke", "black")
    	  .style("fill", "DarkSlateBlue")
     	  .on("mouseover", function(d) { // set the tooltip on mousehover
				tooltip.transition()
					.duration(200)
					.style("opacity", .0);
				tooltip.transition()
					.duration(200)
					.style("opacity", .9)
				tooltip.html("Journal: " + "<a href=http://flourishoa.org/journal/" + d.journal_id + "/ target='_blank'>" + d.journal_name + "</a>"
				+ "<br>Category: " + d.category
				+ "<br>APC: $" + d.price 
				+ "<br>Date: " + formatDate(d.date_stamp1)
				+ "<br>AI Score: " + d.article_influence.toFixed(2))
					.style("left", (d3.event.pageX + 5) + "px")
					.style("top", (d3.event.pageY - 28) + "px");
				function drawQuad() {
				var scaledX = x(d.price);
				var scaledY = y(d.article_influence);
			        svg.append("rect")
                            .attr("id", "better")
                            .attr("x", 0)
                            .attr("y", 0)
                            .attr("width", scaledX)
                            .attr("height", scaledY)
                            .attr("fill", "DarkGreen")
                            .attr("opacity", 0.20)
							.moveToBack();
                    svg.append("rect")
                            .attr("id", "worse")
                            .attr("x", scaledX)
                            .attr("y", scaledY)
                            .attr("width", w - scaledX)
                            .attr("height", h - scaledY)
                            .attr("fill", "Crimson")
                            .attr("opacity", 0.25)	
							.moveToBack();
				}	
					svg.on('click', function() {
						d3.select("#better").remove();
						d3.select("#worse").remove();
						var coords = d3.mouse(this);
						drawQuad();
						})
			})

	circle.exit().remove();

	circle.enter().append("circle")
    	  .attr("cx", function(d) { return x(d.price);  })
    	  .attr("cy", function(d) { return y(d.article_influence);  })
    	  .attr("r", 4.5)
		  .style("stroke-width", 2)
    	  .style("stroke", "black")
    	  .style("fill", "DarkSlateBlue")
		  .style("opacity", 0.6)
    	  .on("mouseover", function(d) {
				tooltip.transition()
					.duration(200)
					.style("opacity", .9);
				tooltip.transition()
					.duration(200)
					.style("opacity", .9)
				tooltip.html("Journal: " + "<a href=http://flourishoa.org/journal/" + d.journal_id + "/ target='_blank'>" + d.journal_name + "</a>"
				+ "<br>Category: " + d.category
				+ "<br>APC: $" + d.price 
				+ "<br>Date: " + formatDate(d.date_stamp1)
				+ "<br>AI Score: " + d.article_influence.toFixed(2))
					.style("left", (d3.event.pageX + 5) + "px")
					.style("top", (d3.event.pageY - 28) + "px");
					function drawQuad() {
						var scaledX = x(d.price);
						var scaledY = y(d.article_influence);
			        	svg.append("rect")
                            .attr("id", "better")
                            .attr("x", 0)
                            .attr("y", 0)
                            .attr("width", scaledX)
                            .attr("height", scaledY)
                            .attr("fill", "DarkGreen")
                            .attr("opacity", 0.20)
							.moveToBack();
                    	svg.append("rect")
                            .attr("id", "worse")
                            .attr("x", scaledX)
                            .attr("y", scaledY)
                            .attr("width", w - scaledX)
                            .attr("height", h - scaledY)
                            .attr("fill", "Crimson")
                            .attr("opacity", 0.25)
							.moveToBack();
						}	
					svg.on('click', function() {
						d3.select("#better").remove();
            			d3.select("#worse").remove();
        				var coords = d3.mouse(this);
       					drawQuad();
						})
                   
			})

}  


// Redraw vis if drop-down menu is used
function filterType(mtype) {
	var patt = new RegExp("all");
	var res = patt.test(mtype.toLowerCase());
		if(res){
			tooltip.transition()
					.duration(500)
					.style("opacity", 0);
					d3.select("#better").remove();
            		d3.select("#worse").remove();
			drawVis(dataset);
		} else{
			var ndata = dataset.filter(function(d) {
				console.log(mtype)
			return d["category"].toLowerCase() == mtype.toLowerCase(); // lowercase all strings
				});	
			tooltip.transition()
					.duration(500)
					.style("opacity", 0);
					d3.select("#better").remove();
            		d3.select("#worse").remove();
			drawVis(ndata);
		}
}