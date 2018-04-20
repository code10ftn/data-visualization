var root = bird_svg;
var zoomBird = d3.behavior
    .zoom()
    .on('zoom.zoom', function () {
        console.trace("zoom", d3.event.translate, d3.event.scale);
        root.attr('transform',
            'translate(' + d3.event.translate + ')'
            + 'scale(' + d3.event.scale + ')');
    });

function zoomFit(paddingPercent, transitionDuration, zoom, root) {
    var bounds = root.node().getBBox();
    var parent = root.node().parentElement;
    var fullWidth = parent.clientWidth,
        fullHeight = parent.clientHeight;
    var width = bounds.width,
        height = bounds.height;
    var midX = bounds.x + width / 2,
        midY = bounds.y + height / 2;
    if (width == 0 || height == 0) return; // nothing to fit
    var scale = (paddingPercent || 0.75) / Math.max(width / fullWidth, height / fullHeight);
    var translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];

    console.trace("zoomFit", translate, scale);
    root
        .transition()
        .duration(transitionDuration || 0) // milliseconds
        .call(zoom.translate(translate).scale(scale).event);
}

bird_force.on('end', zoomOut);

function zoomOut() {
    bird_force.stop();
    zoomFit(0.95, 500, zoomBird, root);
    root.selectAll('.node').on('mousedown.drag', null);
}