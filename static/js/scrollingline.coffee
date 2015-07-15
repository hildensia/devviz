w = 500
h = 300
x = null
y = null
intervalTime = 100

data = d3.range(100).map((n) -> Math.round(Math.random() * 100))

setInterval(
  () ->
#    data.push(Math.round(Math.random() * 100))
#    data.shift()
    calculate_scales()
    redraw()
, intervalTime)

calculate_scales = () ->
  x = d3.scale.linear().domain([0, data.length]).range([0, w])
  y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0])

calculate_scales()

vis = d3.select("body")
.append("svg:svg")
.attr("width", w)
.attr("height", h)
.append("svg:g")

path = d3.svg.line()
.x((d, i) -> x(i))
.y((d) -> y(d))
.interpolate("monotone")

vis.selectAll("path")
.data([data])
.enter()
.append("svg:path")
.attr("d", path)
.attr("fill", "none")
.attr("stroke", "#000")

redraw = () ->
  vis.selectAll("path")
  .data([data])
  .attr("transform", "translate(#{x(1) - x(0)})")
  .attr("d", path)
  .transition()
  .ease("linear")
  .duration(intervalTime)
