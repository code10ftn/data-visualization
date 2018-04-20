function display_graph(svg, links) {
    var nodes = {};
    links.forEach(function(link) {
        link.source = nodes[link.source] || (nodes[link.source] = {
            name: link.source,
            title: link.source.split('|')[1].split('+'),
            ajdi: 'a' + link.source.split('|')[0].replace(/[^0-9a-z]/gi, 't'),
            selected: link.source.split('|')[2]
        });
        link.target = nodes[link.target] || (nodes[link.target] = {
            name: link.target,
            title: link.target.split('|')[1].split('+'),
            ajdi: 'a' + link.target.split('|')[0].replace(/[^0-9a-z]/gi, 't'),
            selected: link.target.split('|')[2]
        });
    });
    svg.append('svg:defs').selectAll('markers').data(['end']).enter().append('svg:marker').attr('id', String).attr('viewBox', '0 -5 10 10').attr('refX', 11).attr('refY', -0.35).attr('markerWidth', 4).attr('markerHeight', 4).attr('orient', 'auto').append('svg:path').attr('d', 'M0,-5L10,0L0,5');
    var force = d3.layout.force().nodes(d3.values(nodes)).links(links).distance(100).charge(-300).start();
    var link = svg.selectAll('.link').data(links).enter().append('line').attr('class', 'link').attr('x1', function(d) {
        return d.source.x;
    }).attr('y1', function(d) {
        return d.source.y;
    }).attr('x2', function(d) {
        return d.target.x;
    }).attr('y2', function(d) {
        return d.target.y;
    }).attr('id', function(d) {
        return d.target.ajdi + 'separator' + d.source.ajdi
    });
    svg.selectAll('.link').data(links).each(function() {
        if (this.id.split('separator')[0] != this.id.split('separator')[1]) {
            d3.select(this).attr('marker-end', 'url(#end)');
        }
    });
    var node = svg.selectAll('.node').data(force.nodes()).enter().append('g').attr('class', 'node').attr('id', function(d) {
        return d.ajdi
    }).call(force.drag);
    node.append('rect').attr('class', 'node').attr('x', 0).attr('y', 0).attr('width', 43).attr('height', function(d) {
        return (d.title.length * 2) + 3
    }).style('stroke', function(d) {
        if (d.selected === 'True') return 'red';
    });
    node.on('mousedown', function(d) {
        d3.event.stopPropagation();
    });
    svg.selectAll('.node').each(function(d) {
        showAttr(d);
    });

    function showAttr(d) {
        for (var i = 0; i < d.title.length; i++) {
            svg.select('g#' + d.ajdi).append('text').attr('dx', 2).attr('dy', String(i + 1) + 'em').attr('class', 'blackSmall').text(function(d) {
                return d.title[i]
            });
        }
    }
    force.on('tick', function() {
        link.attr('x1', function(d) {
            return d.source.x;
        }).attr('y1', function(d) {
            return d.source.y;
        }).attr('x2', function(d) {
            return d.target.x;
        }).attr('y2', function(d) {
            return d.target.y;
        });
        node.attr('transform', function(d) {
            return 'translate(' + d.x + ',' + d.y + ')';
        })
    });

    return force;
}