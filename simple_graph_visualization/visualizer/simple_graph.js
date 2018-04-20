function display_graph(svg, links){
    var nodes = {};
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {
            name: link.source,
            title: link.source.split('|')[1],
            selected: link.source.split('|')[2],
            ajdi: 'a' + link.source.split('|')[0].replace(/[^0-9a-z]/gi, 't')
        });
        link.target = nodes[link.target] || (nodes[link.target] = {
            name: link.target,
            title: link.target.split('|')[1],
            selected: link.target.split('|')[2],
            ajdi: 'a' + link.target.split('|')[0].replace(/[^0-9a-z]/gi, 't')
        });
    });
    svg.append("svg:defs").selectAll("markers").data(["end"]).enter().append("svg:marker").attr("id", String).attr('viewBox', '0 -5 10 10').attr('refX', 15).attr('refY', -0.27).attr('markerWidth', 6).attr('markerHeight', 6).attr('orient', 'auto').append('svg:path').attr('d', 'M0,-5L10,0L0,5').attr('class', 'arrow');
    var force = d3.layout.force().nodes(d3.values(nodes)).links(links).distance(100).charge(-300).start().on('end', function() {
        console.log('ended!');
        console.log(force.size());
    });
    var link = svg.selectAll('.link').data(links).enter().append('line').attr('class', 'link').attr("x1", function(d) {
        return d.source.x;
    }).attr("y1", function(d) {
        return d.source.y;
    }).attr("x2", function(d) {
        return d.target.x;
    }).attr("y2", function(d) {
        return d.target.y;
    }).attr('id', function(d) {
        return d.target.ajdi + 'razmak' + d.source.ajdi
    });
    svg.selectAll('.link').data(links).each(function() {
        if (this.id.split('razmak')[0] != this.id.split('razmak')[1]) {
            d3.select(this).attr("marker-end", "url(#end)");
        }
    });
    var node = svg.selectAll('.node').data(force.nodes()).enter().append('g').attr('class', 'node').call(force.drag);
    node.append('circle').attr("x", function(d) {
        return d.x;
    }).attr("y", function(d) {
        return d.y;
    }).attr("r", 5).style('stroke', function(d) {
        if (d.selected === 'True') return 'red';
    });
    node.append("text").attr("dx", 8).attr("dy", ".35em").attr('class', 'black').text(function(d) {
        return d.title
    }).style('stroke', function(d) {
        if (d.selected === 'True') return 'red';
    }).style('fill', function(d) {
        if (d.selected === 'True') return 'red';
    });
    node.on('mousedown', function(d) {
        d3.event.stopPropagation();
    });
    force.on("tick", function() {
        link.attr("x1", function(d) {
            return d.source.x;
        }).attr("y1", function(d) {
            return d.source.y;
        }).attr("x2", function(d) {
            return d.target.x;
        }).attr("y2", function(d) {
            return d.target.y;
        });
        node.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });
    });
    return force;
}