    // A practical solution (covering all browsers):
    var w = window.innerWidth
    || document.documentElement.clientWidth
    || document.body.clientWidth;

    var h = window.innerHeight
    || document.documentElement.clientHeight
    || document.body.clientHeight;

    var vis1 = d3.select("body").append("svg:svg").attr("width", w).attr("height", h).call(d3.zoom().on("zoom", function () {vis.attr("transform", d3.event.transform);})).on("dblclick.zoom", null);

    var vis = vis1.append("g");

    var nodes = [];
    var links = [];

    var selected = null;

    d3.json("http://127.0.0.1:8000/api/person/?format=json").then(function(json) {
    nodes = json;

    d3.json("http://127.0.0.1:8000/api/links/?format=json").then(function(json) {
      {for (i = 0; i < json.length; i++) {
      {for (j = 0; j < json[i].data.length; j++) {
        links.push(json[i].data[j])}};
    }};

    function getUnion(node) {
    return links.reduce(function (union, link) {
      if (link.type === "union" && (link.target.id === node.id || link.source.id === node.id)) {
        union.push(link.target.id)
      }
      return union
      },
      [node.id]
    )
    }

    function getChildren(node) {
    return links.reduce(function (children, link) {
      if (link.source.id === node.id && link.type === "children") {
        children.push(link.target.id)
      }
      return children
      },
      []
    )
    }

    function getParents(node) {
    return links.reduce(function (parents, link) {
      if (link.target.id === node.id && link.type === "children") {
        parents.push(link.source.id)
      }
      return parents
      },
      []
    )
    }

    function isNeighborLink(node, link) {
      if(node === null){
        return false;
      }
      return link.target.id === node.id || link.source.id === node.id
    }

    function getNodeColor(node, union, children, parents) {
      if (Array.isArray(union) && Array.isArray(children) && Array.isArray(parents)) {
        return union.indexOf(node.id) > -1 ? '#fbb831' : '#689ba5' && children.indexOf(node.id) > -1 ? '#5bc8c1' : '#689ba5' && parents.indexOf(node.id) > -1 ? '#aaba6a' : '#689ba5'
      } else { return '#689ba5' }
    }
    
    function colorstandartlink(link){
      if (link.type === 'union'){
          return "#6eba6a";
        } else {
          return "rgba(50, 50, 50, 0.2)";
        }
    }

    function getLinkColor(node, link) {
      if (isNeighborLink(node, link)){ 
        if (link.type === 'union'){
          return "#ba6a6a";
        }
        else {
          return "#aaba6a"}
        }
      else {
        return colorstandartlink(link)
      }
    }
    
    function getTextColor(node, union, children, parents) {
      if (Array.isArray(union) && Array.isArray(children) && Array.isArray(parents)){
        return union.indexOf(node.id) > -1 ? '#fbb831' : 'black' && children.indexOf(node.id) > -1 ? '#aaba6a' : 'black' && parents.indexOf(node.id) > -1 ? '#aaba6a' : 'black'
      }else{
        return "black";
      }
    }

    function selectNode(selectedNode) {
    if(selected === selectedNode){
      selected = null;
      var union = null;
      var children = null;
      var parents = null;
      // we modify the styles to undo highlight
      nodeElements.attr('fill', function (node) { return getNodeColor(node, union, children, parents) })
      // nodeElements.label.style('fill', function (node) { return getTextColor(node, union, children, parents) })
      linkElements.attr('stroke', function (link) { return getLinkColor(selected, link) })
    }else{
      var union = getUnion(selectedNode);
      var children = getChildren(selectedNode);
      var parents = getParents(selectedNode);
      // we modify the styles to highlight selected nodes
      nodeElements.attr('fill', function (node) { return getNodeColor(node, union, children, parents) })
      // nodeElements.label.style('fill', function (node) { return getTextColor(node, union, children, parents) })
      linkElements.attr('stroke', function (link) { return getLinkColor(selectedNode, link) })
      selected = selectedNode;
      }	
    }

    // Credits to https://bl.ocks.org/mapio/53fed7d84cd1812d6a6639ed7aa83868

    var nodesbyid = {}
    for (var i = 0; i < nodes.length; i++){
      nodesbyid[
        nodes[i]["id"]] =  i
    }
    
    var adjlist = {};
    for(var i = 0; i < links.length; i++) {
      adjlist[nodesbyid[links[i].source] + "-" + nodesbyid[links[i].target]] = true;
      adjlist[nodesbyid[links[i].target] + "-" + nodesbyid[links[i].source]] = true;

      links[i].source = nodesbyid[links[i].source];
      links[i].target = nodesbyid[links[i].target];				
    };
    
    function neigh(a, b) {
        return a == b || adjlist[a + "-" + b];
    }

    
    var label = {
        'nodes': [],
        'links': []
    };

    nodes.forEach(function(d, i) {
        label.nodes.push({node: d});
        label.nodes.push({node: d});
        label.links.push({
            source: i * 2,
            target: i * 2 + 1
        });
    });
        
    var labelLayout = d3.forceSimulation(label.nodes)
        .force("charge", d3.forceManyBody().strength(-60))
        .force("link", d3.forceLink(label.links).distance(10).strength(2));

    var graphLayout = d3.forceSimulation(nodes)
        .force("charge", d3.forceManyBody().strength(-3000))
        .force("center", d3.forceCenter(w / 2, h / 2))
        .force("x", d3.forceX(w / 2).strength(1))
        .force("y", d3.forceY(h / 2).strength(1))
        .force("link", d3.forceLink(links).id(function(d) {return d.index; }).distance(50).strength(1))
        .on("tick", ticked);

      
    function dblclick(d, i) {
      if(d.fixed){
        d.fx = null;
        d.fy = null;
        d3.select(this).classed("fixed", d.fixed = false);
      }
    }

    var node_drag = d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);



    function dragstarted(d) {
        d3.event.sourceEvent.stopPropagation();
        if (!d3.event.active) graphLayout.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) graphLayout.alphaTarget(0);
        d.fixed = true;
    }

      

		var	linkElements = vis.append("g")
			.attr("class", "links")
			.selectAll("line")
			.data(links)
			.enter().append("line")
				.attr("stroke-width", 5)
				.attr("stroke", function (d) {return colorstandartlink(d)});

		var	nodeElements = vis.append("g")
				.attr("class", "nodes")
				.selectAll("circle")
        .data(nodes)
        .enter().append("circle")
          .attr("r", 12)
          .attr("fill", getNodeColor)
          .on('click', selectNode)
          .on("dblclick", dblclick)
          .call(node_drag)

    nodeElements.on("mouseover", focus).on("mouseout", unfocus);

    var labelNode = vis.append("g").attr("class", "labelNodes")
    .selectAll("text")
    .data(label.nodes)
    .enter()
    .append("text")
    .text(function(d, i) { return i % 2 == 0 ? "" : d.node.name; })
    .style("fill", "#555")
    .style("font-family", "Arial")
    .style("font-size", 12)
    .style("pointer-events", "none"); // to prevent mouseover/drag capture
    
    function ticked() {
      nodeElements.call(updateNode);
      linkElements.call(updateLink);

      labelLayout.alphaTarget(0.3).restart();
      labelNode.each(function(d, i) {
          if(i % 2 == 0) {
            if (d.node.x < w/2){
              d.x = d.node.x - Math.min(d.node.name.length*9*(w/2 - d.node.x)/(w/2), d.node.name.length*5)
            } else {
              d.x = d.node.x;
            }
              
              d.y = d.node.y;
          } else {
              var b = this.getBBox();

              var diffX = d.x - d.node.x;
              var diffY = d.y - d.node.y;

              var dist = Math.sqrt(diffX * diffX + diffY * diffY);

              var shiftX = b.width * (diffX - dist) / (dist * 2);
              shiftX = Math.max(-b.width, Math.min(0, shiftX));
              var shiftY = 16;
              this.setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
          }
      });
      labelNode.call(updateNode);

}

    function fixna(x) {
      if (isFinite(x)) return x;
      return 0;
    }

    function focus(d) {
      var index = d3.select(d3.event.target).datum().index;
        nodeElements.style("opacity", function(o) {
          return neigh(index, o.index) ? 1 : 0.1;
      });
        labelNode.attr("display", function(o) {
        return neigh(index, o.node.index) ? "block": "none";
      });
        linkElements.style("opacity", function(o) {
          return o.source.index == index || o.target.index == index ? 1 : 0.1;
      });
    }

    function unfocus() {
      labelNode.attr("display", "block");
      nodeElements.style("opacity", 1);
      linkElements.style("opacity", 1);
    }

    function updateLink(link) {
      link.attr("x1", function(d) { return fixna(d.source.x); })
          .attr("y1", function(d) { return fixna(d.source.y); })
          .attr("x2", function(d) { return fixna(d.target.x); })
          .attr("y2", function(d) { return fixna(d.target.y); });
    }

    function updateNode(node) {
      node.attr("transform", function(d) {
          return "translate(" + fixna(d.x) + "," + fixna(d.y) + ")";
      });
    }
    });
    });