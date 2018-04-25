////////////////////////////////////////////////////////////
//////////////////////// Set-up ////////////////////////////
////////////////////////////////////////////////////////////

//Chart variables
var startYear,
	years, //save height per year
	rectWidth,
	rectHeight,
	rectCorner,
	currentYear = 2015,
	chosenYear = currentYear,
	chosenYearOld = currentYear,
	optArray, //for search box
	inSearch = false, //is the search box being used - for tooltip
	selectedArtist; //for search box and highlighting
	fileName = "profiles.csv";	

	
//Width and Height of the SVG
var	wind = window,
	d = document,
	e = d.documentElement,
	g = d.getElementsByTagName('body')[0],
	maxWidth = 1200, //Maximum width of the chart, regardless of screen size
	maxHeight = 800, //Maximum height of the chart, regardless of screen size
	w = Math.min(maxWidth, wind.innerWidth || e.clientWidth || g.clientWidth),
	h = Math.min(maxHeight, wind.innerHeight|| e.clientHeight|| g.clientHeight);

//Offsets needed to properly position elements
var xOffset = Math.max(0, ((wind.innerWidth || e.clientWidth || g.clientWidth)-maxWidth)/2),
	yOffset = Math.max(0, ((wind.innerHeight|| e.clientHeight|| g.clientHeight)-maxHeight)/2)

//Find the offsets due to other divs
var offsets = document.getElementById('chart').getBoundingClientRect();
	
//SVG locations
var margin = {top: 120, right: 40, bottom: 20, left: 100},
	padding = 40,
    width = w - margin.left - margin.right - padding,
    height = h - margin.top - margin.bottom - padding - offsets.top;

////////////////////////////////////////////////////////////
////////////////// Reposition elements /////////////////////
////////////////////////////////////////////////////////////

//Change note location
//d3.select("#note")
//	.style("top", (height + margin.top + margin.bottom + 40)+"px")
//	.style("left", (xOffset + 20)+"px");
	
//Change intro location
d3.select("#intro")
	.style("left", (xOffset + 20)+"px");

d3.select("#link")
	.style("right",(xOffset + 20) + "px");

// d3.select("#artist-info")
// 	.style("left", (xOffset + 20)+"px")
// 	.style("width", width+"px");

//Change search box
var searchWidth = Math.min(300,width/2);
d3.select("#searchBoxWrapper")
	.style("left", (width/2 + xOffset + padding + margin.left - searchWidth/2)+"px")
	.style("width", searchWidth+"px");
	
// if (handheld == false) {
				
// 	//If the user clicks anywhere while in search mode, remove the search
// 	d3.select("body").on("click", function() { 
// 		if(inSearch) {
// 			inSearch = false;
// 			searchArtist("");
// 		}		
// 	});
// }
	
//////////////////////////////////////////////////////
///////////// Initialize Axes & Scales ///////////////
//////////////////////////////////////////////////////
	
var x = d3.scaleBand()
    .rangeRound([0, width/2])
    .padding(0.5);

var y = d3.scaleLinear()
    .range([height, 0]);

var xAxis = d3.axisBottom(x);

var yAxis = d3.axisLeft(y)
	.tickFormat(d3.format("d"));


var x2 = d3.scaleLinear()
    .rangeRound([0, width/2]);

var y2 = d3.scaleBand()
    .range([height, 0]);

var xAxis2 = d3.axisBottom(x)
	.tickFormat(d3.format("d"));

var yAxis2 = d3.axisLeft(y);	
// //Create colors
// var hexLocation = [
// 	{color:"#007F24", text: "1 - 24", rank: d3.range(1,25)},
// 	{color:"#62BF18", text: "25 - 49", rank: d3.range(25,50)},
// 	{color:"#FFC800", text: "50 - 99", rank: d3.range(50,100)},
// 	{color:"#FF5B13", text: "100 - 249", rank: d3.range(100,250)},
// 	{color:"#E50000", text: "250 - 500", rank: d3.range(250,500)}
// ];
// var hexKey = [];
// hexLocation.forEach(function(d,i) {
// 	hexKey[d.color] = i;
// })
	
// var color = d3.scale.linear()
// 	.domain([1,25,50,100,250,500])
// 	.range(hexLocation.map(function(d) { return d.color; }));

////////////////////////////////////////////////////////////	
///////////////////// Initiate SVG /////////////////////////
////////////////////////////////////////////////////////////

//Initiate outer chart SVG
var barchart = d3.select("#chart").append("svg")
    .attr("width", width/2 + margin.left/2 + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class", "barchart")
  	

var svg = barchart.append("g")
	.attr("transform", "translate(" + margin.left/2 + "," + margin.top/1.5 + ")");

var dotplot = d3.select("#chart").append("svg")
    .attr("width", width/2 + margin.left + margin.right/2)
    .attr("height", height + margin.top + margin.bottom)
    .attr("class", "dotplot")

var svg2 = dotplot
	.append("g")
    .attr("transform", "translate(" + margin.left/2 + "," + margin.top/1.5 + ")");



//Container for all the rectangles
var barContainer = svg.append("g").attr("class","barContainer");

var dotContainer = svg2.append("g").attr("class","dotContainer");


var artist_name = d3.select(".info.name")
var artist_song = d3.select(".info.song")
var artist_genres = d3.select(".info.genres")
var artist_years = d3.select(".info.years")
var artist_score = d3.select(".info.score")

////////////////////////////////////////////////////////////	
///////////////////// Read in data /////////////////////////
////////////////////////////////////////////////////////////

d3.csv(fileName, function(error, data) {

	//Convert to numeric values
	for(var i = 0; i < data.length; i++) { 
		data[i].year_st = +data[i].year_st;
		data[i].year_end = +data[i].year_end;
		data[i].sent_score = +data[i].sent_score;
		data[i].songs = +data[i].songs;
		data[i].album = "" + data[i].album;
	}
		
	//Calculate domains of chart
	//startYear = d3.min(data, function(d) { return d.release; });
	//x.domain([startYear-1,d3.max(data, function(d) { return d.release; })+1]);//.nice();
	//y.domain([0,30]).nice();

	//Keeps track of the height of each year
	// years = d3.range(d3.min(x.domain()),d3.max(x.domain()))
	// 	.map(function(d,i) {
	// 	  return {
	// 		year: d,
	// 		number: 1
	// 	  };
	// 	});

	//Size of the "song" rectangles
	// rectWidth = Math.floor(x.range()[1]/100);
	// rectHeight = Math.min(3,Math.floor(y.range()[0]/50));
	// rectCorner = rectHeight/2;

	//Create x axis
	svg.append("g")
		  .attr("class", "x axis")
		  .attr("transform", "translate(0," + height + ")")
		  .call(xAxis)
		.append("text")
		  .attr("class", "label")
		  .attr("x", width/2)
		  .attr("y", 35)
		  .style("text-anchor", "end")
		  .text("Word");

	//Create y axis
	svg.append("g")
		  .attr("class", "y axis")
		  .call(yAxis)
		.append("text")
		  .attr("class", "label")
		  .attr("transform", "rotate(-90)")
		  .attr("y", 8)
		  .attr("dy", ".71em")
		  .style("text-anchor", "end")
		  .text("Frequency");

	svg2.append("g")
		  .attr("class", "x axis")
		  .attr("transform", "translate(0," + height + ")")
		  .call(xAxis)
		.append("text")
		  .attr("class", "label")
		  .attr("x", width/2)
		  .attr("y", 35)
		  .style("text-anchor", "end")
		  .text("Topic");

	//Create y axis
	svg2.append("g")
		  .attr("class", "y axis")
		  .call(yAxis)
		.append("text")
		  .attr("class", "label")
		  .attr("transform", "rotate(-90)")
		  .attr("y", 8)
		  .attr("dy", ".71em")
		  .style("text-anchor", "end");
	
	barchart.append("text")
		.attr("x", (width / 4))             
        .attr("y", margin.top/2.5)
        .attr("text-anchor", "start")  
        .style("font-size", "16px") 
        .text("Top Words");

    dotplot.append("text")
		.attr("x", (width / 4))             
        .attr("y", margin.top/2.5)
        .attr("text-anchor", "start")  
        .style("font-size", "16px") 
        .text("Topic Scores");
	
	artist_name.data(data).text(d => d.artist)


	artist_song.data(data).text(d => d.songs)

	artist_genres.data(data).text(function(d){
		var genres = JSON.parse(JSON.stringify(eval("(" + d.genres + ")")));
		if (genres.length >= 3) {
			return genres[0] + "\r\n" + genres[1] + "\n" + genres[2];
		}

		if (genres.length == 2) {
			return genres[0] + "\n" + genres[1];
		} 

		if (genres.length == 1) {
			return genres[0];
		}
	});

	artist_years.data(data).text(d => (d.mean_sentiment))

	var json
	var topic

	artist_score.data(data).text(function(d){
		var similar = JSON.parse(JSON.stringify(eval("(" + d.similar + ")")));
		json = JSON.parse(JSON.stringify(eval("(" + d.words + ")")));
		topic = JSON.parse(JSON.stringify(eval("(" + d.topic + ")")));

		if (similar.length >= 3) {
			return similar[0] + "\r\n" + similar[1] + "\n" + similar[2];
		}

		if (similar.length == 2) {
			return similar[0] + "\n" + similar[1];
		} 

		if (similar.length == 1) {
			return similar[0];
		}
	});


	//Create the legend
	// createLegend();

	//Update the search box
	updateSearchbox(data);

	

	y2.domain(topic.map(d => d.topic));
	x2.domain([0,1]);

			// //Create x axis
	

	svg2.select("g.x.axis")
		.call(d3.axisBottom(x2));
	//Create y axis
	svg2.select("g.y.axis")
		  .call(d3.axisLeft(y2))
		  .selectAll(".tick text")
		  .style("text-anchor", "middle")
          .attr("dx", ".75em")
          .attr("dy", "-1em")
		  .attr("transform", "rotate(-90)");

	var barContainer = svg.select(".barContainer");

	var dotContainer = svg2.select(".dotContainer");


	var bars = barContainer.selectAll(".bar")
								.data(json.sort(function(a, b) {return d3.descending(a.count, b.count)}),d => d.count);

	y.domain([0,d3.max(json, d => Math.ceil(d.proportion*1000)/1000)]);
	x.domain(json.map(d => d.word));

	svg.select("g.x.axis")
		.call(d3.axisBottom(x));

	//Create y axis
	svg.select("g.y.axis")
		  .call(d3.axisLeft(y).ticks(7));
	
	var dots = dotContainer.selectAll(".bar")
								.data(topic);

	var lines = svg2.selectAll("lines")
          .data(topic)
          .enter()
          .append("line");


    lines.attr("x1", 0)
          .attr("y1", (d,i) =>  y2(d.topic) + y2.bandwidth()/2)
          .attr("x2", width/2)
          .attr("y2", (d,i) =>  y2(d.topic)+y2.bandwidth()/2)
          .attr("stroke", "#eee")
          .style("stroke-dasharray", ("3, 3")) ;

	//ENTER
	bars.enter().append("rect")
		.attr("class", "bar")
		.attr("rx", rectCorner)
		.attr("ry", rectCorner)
		.attr("width", x.bandwidth())
		.attr("x", function(d) {return x(d.word)})
		.attr("y", height) //setting y at the bottom for the transition effect
		.attr("height", 0)
		.transition()
		.duration(500)
		.attr("height", d => (height - y(d.proportion)))
		.attr("y", function(d) {return y(d.proportion);});


	dots.enter().append("circle")
		.attr("class", "dot")
		.merge(dots)
		.attr("r", 5)
		.attr("cx", 0)
		.attr("cy", d => (y2(d.topic) + y2.bandwidth()/2)) //setting y at the bottom for the transition effect
		.transition()
		.duration(500)
		.attr("cx", function(d) {return x2(d.score)});


	d3.selectAll("#intro")
        .on("click", function () {
          var idx = Math.floor(Math.random() * data.length)
          searchArtist(data[idx].artist)




       })

		
	// //Reset the heights
	// years.forEach(function(value, index) {
	// 	years[index].number = 1;
	// });
	

	// var dots = dotContainer.selectAll(".dot")
	// 			.data(data
	// 					.sort(function(a, b) {return a.rank - b.rank}) 
	// 					, function(d) { return d.rank; });
		
	
	// //ENTER
	// dots.enter().append("rect")
	// 	.attr("class", "dot")
	// 	.attr("width", rectWidth)
	// 	.attr("height", rectHeight)
	// 	.attr("rx", rectCorner)
	// 	.attr("ry", rectCorner)
	// 	.style("fill", function(d) { return color(d.rank); })
	// 	.on("mouseover", showTooltip)
	// 	.on("mouseout", hideTooltip)
	// 	.attr("x", function(d) { return (x(d.release) - rectWidth/2); })
	// 	.attr("y", function(d) {return y(0);})
	// 	.style("opacity",0);

	// dots
	// 	.transition().duration(500)
	// 	.attr("y", function(d) { return y(0); })
	// 	.style("opacity",0)
	// 	.call(endall, function() {
	// 		dots
	// 			.attr("x", function(d) { return (x(d.release) - rectWidth/2); })
	// 			.attr("y", function(d) { return locateY(d); })
	// 			.transition().duration(10).delay(function(d,i) { return i/2; })
	// 			.style("opacity",1);
	// 	});
					
});